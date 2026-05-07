"""AI-powered product recommendation engine using Groq."""
import json
import logging
from .groq_client import groq_client

logger = logging.getLogger(__name__)


def get_recommendations(user, product=None, limit=6):
    """Get personalized product recommendations using Groq AI.
    
    Analyzes user activity history, purchase patterns, and current context
    to generate intelligent product recommendations.
    """
    from accounts.models import UserActivity
    from products.models import Product

    # Gather user context
    activities = UserActivity.objects.filter(user=user).select_related('product')[:20]
    activity_summary = []
    for act in activities:
        if act.product:
            activity_summary.append({
                'action': act.activity_type,
                'product': act.product.name,
                'category': act.product.category.name,
                'brand': act.product.brand,
                'price': str(act.product.price),
            })

    # Get available products
    all_products = Product.objects.filter(is_active=True, stock__gt=0).values(
        'name', 'slug', 'category__name', 'brand', 'price', 'avg_rating', 'discount_percent'
    )[:50]
    product_list = list(all_products)

    current_product_info = ""
    if product:
        current_product_info = f"\nCurrently viewing: {product.name} (Category: {product.category.name}, Brand: {product.brand}, Price: ₹{product.price})"

    prompt = f"""You are an AI recommendation engine for an e-commerce platform.
Based on the user's activity history and available products, recommend exactly {limit} products.

User Activity History:
{json.dumps(activity_summary[:10], indent=2)}
{current_product_info}

Available Products:
{json.dumps(product_list[:30], default=str, indent=2)}

Return a JSON object with key "recommendations" containing an array of product slugs with reasons:
{{"recommendations": [{{"slug": "product-slug", "reason": "brief reason"}}]}}

Focus on:
1. Similar categories to what user has viewed/purchased
2. Complementary products
3. Popular items in their preferred price range
4. Items with good ratings and discounts"""

    result = groq_client.chat_json([
        {"role": "system", "content": "You are a product recommendation AI. Always respond with valid JSON."},
        {"role": "user", "content": prompt}
    ])

    if result and 'recommendations' in result:
        recommended_slugs = [r['slug'] for r in result['recommendations']]
        products = Product.objects.filter(slug__in=recommended_slugs, is_active=True)
        if products.exists():
            return {
                'products': products,
                'reasons': {r['slug']: r.get('reason', '') for r in result['recommendations']}
            }

    # Fallback: return popular products
    fallback = Product.objects.filter(is_active=True).order_by('-total_sold', '-avg_rating')[:limit]
    return {'products': fallback, 'reasons': {}}


def get_similar_products(product, limit=4):
    """Find products similar to the given product."""
    from products.models import Product

    prompt = f"""Given this product:
Name: {product.name}
Category: {product.category.name}
Brand: {product.brand}
Price: ₹{product.price}
Tags: {product.tags}

Find similar products from this catalog that a buyer would also consider:
{list(Product.objects.filter(is_active=True, category=product.category).exclude(pk=product.pk).values('name', 'slug', 'brand', 'price')[:20])}

Return JSON: {{"similar": ["slug1", "slug2", ...]}}"""

    result = groq_client.chat_json([
        {"role": "system", "content": "You are a product similarity AI. Respond with valid JSON only."},
        {"role": "user", "content": prompt}
    ])

    if result and 'similar' in result:
        return Product.objects.filter(slug__in=result['similar'], is_active=True)[:limit]

    return Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).order_by('-avg_rating')[:limit]
