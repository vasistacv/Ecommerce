"""AI-powered price prediction using Groq."""
import json
import logging
from .groq_client import groq_client

logger = logging.getLogger(__name__)


def predict_price(product, days_ahead=30):
    """Predict future price trends for a product.
    
    Returns:
        dict: {current_price, predicted_price, trend, confidence, recommendation, analysis}
    """
    from products.models import PriceHistory

    # Get price history
    history = PriceHistory.objects.filter(product=product).order_by('recorded_at')[:30]
    price_data = [{'price': str(h.price), 'date': str(h.recorded_at.date())} for h in history]

    prompt = f"""Analyze the price history of this product and predict future price trends.

Product: {product.name}
Category: {product.category.name}
Brand: {product.brand}
Current Price: ₹{product.price}
Discount: {product.discount_percent}%
Stock Level: {product.stock}
Total Sold: {product.total_sold}
Average Rating: {product.avg_rating}

Price History (last 30 records):
{json.dumps(price_data, indent=2)}

Prediction Period: Next {days_ahead} days

Return JSON:
{{
    "current_price": {float(product.price)},
    "predicted_price": 0.0,
    "trend": "up/down/stable",
    "confidence": 0.0-1.0,
    "percent_change": 0.0,
    "recommendation": "buy_now/wait/neutral",
    "analysis": "brief analysis of price trend",
    "factors": ["factor1", "factor2"]
}}"""

    result = groq_client.chat_json([
        {"role": "system", "content": "You are a price prediction AI for e-commerce. Analyze price trends and predict future prices. Respond with JSON only. Be realistic in predictions."},
        {"role": "user", "content": prompt}
    ])

    if result:
        return {
            'current_price': float(product.price),
            'predicted_price': result.get('predicted_price', float(product.price)),
            'trend': result.get('trend', 'stable'),
            'confidence': result.get('confidence', 0.5),
            'percent_change': result.get('percent_change', 0),
            'recommendation': result.get('recommendation', 'neutral'),
            'analysis': result.get('analysis', ''),
            'factors': result.get('factors', []),
        }

    return {
        'current_price': float(product.price),
        'predicted_price': float(product.price),
        'trend': 'stable',
        'confidence': 0.5,
        'percent_change': 0,
        'recommendation': 'neutral',
        'analysis': 'Price prediction analysis unavailable.',
        'factors': [],
    }
