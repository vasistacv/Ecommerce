"""AI Chatbot for customer support using Groq."""
import logging
from .groq_client import groq_client

logger = logging.getLogger(__name__)

# System prompt for the chatbot
CHATBOT_SYSTEM_PROMPT = """You are SmartBot, the AI customer support assistant for SmartShop, a premium e-commerce platform.

Your capabilities:
1. Answer questions about products, orders, shipping, and returns
2. Help users find products based on their needs
3. Provide order status information
4. Explain policies (shipping, returns, warranty)
5. Offer product recommendations
6. Handle complaints professionally

Key policies:
- Free shipping on orders over ₹500
- 30-day return policy for unused items
- 18% GST on all products
- Delivery typically within 3-7 business days
- Loyalty points: 1 point per ₹10 spent

Respond in a friendly, professional, and helpful manner. Keep responses concise but informative.
Use emojis sparingly for a friendly tone. If you don't know something, suggest contacting human support.
Never make up product details or order statuses - say you'll need to check."""


def get_chat_response(user_message, conversation_history=None, user=None):
    """Get chatbot response for a user message.
    
    Args:
        user_message: The user's message
        conversation_history: List of previous messages [{role, content}]
        user: Django User object for context
    
    Returns:
        str: The chatbot's response
    """
    messages = [{"role": "system", "content": CHATBOT_SYSTEM_PROMPT}]

    # Add user context if available
    if user and user.is_authenticated:
        user_context = f"\n\nUser Info: {user.first_name} {user.last_name} (Member since {user.date_joined.strftime('%B %Y')})"
        try:
            profile = user.profile
            user_context += f", Loyalty Points: {profile.loyalty_points}"
            if profile.is_premium:
                user_context += " (Premium Member)"
        except Exception:
            pass

        # Recent orders
        from orders.models import Order
        recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:3]
        if recent_orders:
            user_context += "\nRecent Orders:"
            for order in recent_orders:
                user_context += f"\n- {order.order_number}: {order.get_status_display()} (₹{order.total})"

        messages[0]["content"] += user_context

    # Add conversation history
    if conversation_history:
        messages.extend(conversation_history[-6:])  # Last 6 messages for context

    # Add current message
    messages.append({"role": "user", "content": user_message})

    response = groq_client.chat(messages, temperature=0.7, max_tokens=512)

    if response:
        return response
    return "I'm sorry, I'm having trouble connecting right now. Please try again in a moment, or contact our support team at support@smartshop.com 📧"
