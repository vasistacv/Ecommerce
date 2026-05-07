"""AI Engine API views."""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .chatbot import get_chat_response
from .recommender import get_recommendations
from .fraud_detection import analyze_order_fraud
from .sentiment import analyze_sentiment
from .price_prediction import predict_price
from .fake_review import detect_fake_review


@csrf_exempt
@require_POST
def chat_api(request):
    """AI Chatbot API endpoint."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        history = data.get('history', [])

        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        response = get_chat_response(
            user_message=message,
            conversation_history=history,
            user=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({
            'success': True,
            'response': response,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def recommend_api(request):
    """Get AI-powered product recommendations."""
    try:
        product_slug = request.GET.get('product')
        product = None
        if product_slug:
            from products.models import Product
            product = Product.objects.filter(slug=product_slug).first()

        result = get_recommendations(request.user, product=product, limit=6)
        products = result['products']
        reasons = result['reasons']

        data = [{
            'id': str(p.id),
            'name': p.name,
            'slug': p.slug,
            'price': str(p.price),
            'sale_price': str(p.sale_price),
            'discount': str(p.discount_percent),
            'rating': str(p.avg_rating),
            'image': p.image.url if p.image else '',
            'reason': reasons.get(p.slug, ''),
        } for p in products]

        return JsonResponse({'success': True, 'recommendations': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_POST
def fraud_check_api(request):
    """Check an order for fraud."""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        if not order_id:
            return JsonResponse({'error': 'order_id is required'}, status=400)

        from orders.models import Order
        order = Order.objects.get(pk=order_id, user=request.user)
        result = analyze_order_fraud(order)

        # Update order
        order.fraud_score = result['score']
        order.fraud_flagged = result['flagged']
        order.fraud_reason = ', '.join(result['reasons'])
        order.save(update_fields=['fraud_score', 'fraud_flagged', 'fraud_reason'])

        return JsonResponse({'success': True, **result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def sentiment_api(request):
    """Analyze review sentiment."""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        title = data.get('title', '')
        review_id = data.get('review_id')

        if not text:
            return JsonResponse({'error': 'text is required'}, status=400)

        result = analyze_sentiment(text, title)

        # Update review if ID provided
        if review_id:
            from products.models import Review
            try:
                review = Review.objects.get(pk=review_id)
                review.sentiment_score = result['score']
                review.sentiment_label = result['label']
                review.save(update_fields=['sentiment_score', 'sentiment_label'])
            except Review.DoesNotExist:
                pass

        return JsonResponse({'success': True, **result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def price_predict_api(request):
    """Predict product price."""
    try:
        product_slug = request.GET.get('product')
        days = int(request.GET.get('days', 30))

        if not product_slug:
            return JsonResponse({'error': 'product slug is required'}, status=400)

        from products.models import Product
        product = Product.objects.get(slug=product_slug)
        result = predict_price(product, days_ahead=days)

        return JsonResponse({'success': True, **result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def fake_review_api(request):
    """Detect fake reviews."""
    try:
        data = json.loads(request.body)
        review_id = data.get('review_id')

        if not review_id:
            return JsonResponse({'error': 'review_id is required'}, status=400)

        from products.models import Review
        review = Review.objects.get(pk=review_id)
        result = detect_fake_review(review)

        # Update review
        review.is_fake = result['is_fake']
        review.fake_confidence = result['confidence']
        review.save(update_fields=['is_fake', 'fake_confidence'])

        return JsonResponse({'success': True, **result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
