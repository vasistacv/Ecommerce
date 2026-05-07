"""Shopping cart views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product
from accounts.models import UserActivity


@login_required
def cart_view(request):
    """Display shopping cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    return render(request, 'cart/cart.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    # Track activity
    UserActivity.objects.create(
        user=request.user, activity_type='cart', product=product
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart.total_items,
            'cart_total': str(cart.total),
        })

    messages.success(request, f'"{product.name}" added to cart! 🛒')
    return redirect('cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    else:
        if quantity > cart_item.product.stock:
            quantity = cart_item.product.stock
            messages.warning(request, f'Only {quantity} items available.')
        cart_item.quantity = quantity
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = cart_item.cart
        return JsonResponse({
            'success': True,
            'line_total': str(cart_item.line_total),
            'subtotal': str(cart.subtotal),
            'tax': str(cart.tax),
            'total': str(cart.total),
            'cart_count': cart.total_items,
        })

    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'message': f'{product_name} removed.',
            'subtotal': str(cart.subtotal),
            'tax': str(cart.tax),
            'total': str(cart.total),
            'cart_count': cart.total_items,
        })

    messages.info(request, f'"{product_name}" removed from cart.')
    return redirect('cart')


@login_required
@require_POST
def clear_cart(request):
    """Clear all items from cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.info(request, 'Cart cleared.')
    return redirect('cart')
