"""AI-powered fraud detection engine using Groq."""
import json
import logging
from .groq_client import groq_client

logger = logging.getLogger(__name__)


def analyze_order_fraud(order):
    """Analyze an order for potential fraud using AI.
    
    Returns:
        dict: {score: 0-1, flagged: bool, reasons: [str], recommendation: str}
    """
    # Gather order context
    order_data = {
        'order_number': order.order_number,
        'total': str(order.total),
        'items_count': order.items.count(),
        'shipping_city': order.shipping_city,
        'shipping_state': order.shipping_state,
        'payment_status': order.payment_status,
    }

    # User history
    user = order.user
    from orders.models import Order
    past_orders = Order.objects.filter(user=user).exclude(pk=order.pk)
    user_data = {
        'username': user.username,
        'member_since': str(user.date_joined.date()),
        'total_past_orders': past_orders.count(),
        'past_order_total': str(sum(float(o.total) for o in past_orders)),
        'email_verified': user.email != '',
    }

    # Order items
    items = list(order.items.values('product_name', 'quantity', 'unit_price', 'total_price'))

    prompt = f"""Analyze this e-commerce order for potential fraud. Consider:
1. Order value vs user history
2. Unusual item combinations or quantities
3. New account with high-value order
4. Shipping location patterns

Order Data:
{json.dumps(order_data, default=str, indent=2)}

User Data:
{json.dumps(user_data, default=str, indent=2)}

Order Items:
{json.dumps(items, default=str, indent=2)}

Return JSON:
{{"score": 0.0-1.0, "flagged": true/false, "reasons": ["reason1"], "recommendation": "approve/review/reject"}}

Score guidelines:
- 0.0-0.3: Low risk (approve)
- 0.3-0.6: Medium risk (review)
- 0.6-1.0: High risk (flag)"""

    result = groq_client.chat_json([
        {"role": "system", "content": "You are a fraud detection AI for an e-commerce platform. Analyze orders and respond with JSON only. Be balanced - don't flag legitimate orders."},
        {"role": "user", "content": prompt}
    ])

    if result:
        score = result.get('score', 0.1)
        return {
            'score': score,
            'flagged': result.get('flagged', False),
            'reasons': result.get('reasons', []),
            'recommendation': result.get('recommendation', 'approve'),
        }

    # Default: low risk
    return {
        'score': 0.1,
        'flagged': False,
        'reasons': ['Analysis unavailable - defaulting to low risk'],
        'recommendation': 'approve',
    }
