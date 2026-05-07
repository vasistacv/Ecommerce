"""Cart context processor to make cart count available in all templates."""

def cart_count(request):
    """Add cart item count to template context."""
    if request.user.is_authenticated:
        try:
            from .models import Cart
            cart = Cart.objects.get(user=request.user)
            return {'cart_item_count': cart.total_items}
        except Cart.DoesNotExist:
            pass
    return {'cart_item_count': 0}
