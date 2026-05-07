"""Admin analytics dashboard views."""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, F, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from orders.models import Order
from products.models import Product, Review, Category
from accounts.models import UserActivity
from django.contrib.auth.models import User
from payments.models import Payment


@staff_member_required
def dashboard(request):
    """Main admin analytics dashboard."""
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_7_days = now - timedelta(days=7)

    # Key metrics
    total_revenue = Order.objects.filter(
        payment_status='paid'
    ).aggregate(total=Sum('total'))['total'] or 0

    monthly_revenue = Order.objects.filter(
        payment_status='paid', created_at__gte=last_30_days
    ).aggregate(total=Sum('total'))['total'] or 0

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_users = User.objects.count()
    new_users_week = User.objects.filter(date_joined__gte=last_7_days).count()
    total_products = Product.objects.filter(is_active=True).count()
    low_stock = Product.objects.filter(stock__lte=F('min_stock_alert'), is_active=True).count()

    avg_order_value = Order.objects.filter(
        payment_status='paid'
    ).aggregate(avg=Avg('total'))['avg'] or 0

    # Revenue by day (last 30 days)
    daily_revenue = Order.objects.filter(
        payment_status='paid', created_at__gte=last_30_days
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        revenue=Sum('total'), orders=Count('id')
    ).order_by('date')

    # Top products
    top_products = Product.objects.filter(is_active=True).order_by('-total_sold')[:10]

    # Top categories
    top_categories = Category.objects.annotate(
        total_revenue=Sum('products__price'),
        product_count=Count('products')
    ).order_by('-product_count')[:5]

    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # Fraud alerts
    fraud_orders = Order.objects.filter(fraud_flagged=True).order_by('-created_at')[:5]

    # Review stats
    total_reviews = Review.objects.count()
    fake_reviews = Review.objects.filter(is_fake=True).count()
    avg_sentiment = Review.objects.filter(
        sentiment_score__isnull=False
    ).aggregate(avg=Avg('sentiment_score'))['avg'] or 0

    # Payment methods distribution
    payment_methods = Payment.objects.filter(
        status='completed'
    ).values('payment_method').annotate(
        count=Count('id'), total=Sum('amount')
    ).order_by('-count')

    # Order status distribution
    order_statuses = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    context = {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_users': total_users,
        'new_users_week': new_users_week,
        'total_products': total_products,
        'low_stock': low_stock,
        'avg_order_value': round(avg_order_value, 2),
        'daily_revenue': list(daily_revenue),
        'top_products': top_products,
        'top_categories': top_categories,
        'recent_orders': recent_orders,
        'fraud_orders': fraud_orders,
        'total_reviews': total_reviews,
        'fake_reviews': fake_reviews,
        'avg_sentiment': round(avg_sentiment, 2),
        'payment_methods': list(payment_methods),
        'order_statuses': list(order_statuses),
    }
    return render(request, 'analytics/dashboard.html', context)


@staff_member_required
def revenue_data(request):
    """API endpoint for revenue chart data."""
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    data = Order.objects.filter(
        payment_status='paid', created_at__gte=start_date
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        revenue=Sum('total'), orders=Count('id')
    ).order_by('date')

    return JsonResponse({
        'labels': [str(d['date']) for d in data],
        'revenue': [float(d['revenue']) for d in data],
        'orders': [d['orders'] for d in data],
    })
