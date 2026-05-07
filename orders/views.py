"""Order views - checkout, order history, tracking."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, OrderTracking
from cart.models import Cart
from accounts.models import UserActivity


@login_required
def checkout(request):
    """Checkout page."""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    items = cart.items.select_related('product').all()
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    addresses = request.user.addresses.all()

    if request.method == 'POST':
        # Get shipping info
        shipping_name = request.POST.get('shipping_name', '')
        shipping_address = request.POST.get('shipping_address', '')
        shipping_city = request.POST.get('shipping_city', '')
        shipping_state = request.POST.get('shipping_state', '')
        shipping_zip = request.POST.get('shipping_zip', '')
        shipping_phone = request.POST.get('shipping_phone', '')

        if not all([shipping_name, shipping_address, shipping_city, shipping_state, shipping_zip, shipping_phone]):
            messages.error(request, 'Please fill in all shipping details.')
            return render(request, 'orders/checkout.html', {
                'cart': cart, 'items': items, 'addresses': addresses,
            })

        # Create order
        subtotal = cart.subtotal
        tax = cart.tax
        shipping_cost = 0 if float(subtotal) > 500 else 49
        total = float(subtotal) + tax + shipping_cost

        order = Order.objects.create(
            user=request.user,
            shipping_name=shipping_name,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_zip=shipping_zip,
            shipping_phone=shipping_phone,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping_cost,
            total=total,
            estimated_delivery=timezone.now().date() + timedelta(days=5),
        )

        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_sku=item.product.sku,
                quantity=item.quantity,
                unit_price=item.product.sale_price,
                total_price=item.line_total,
            )
            # Update stock
            item.product.stock -= item.quantity
            item.product.total_sold += item.quantity
            item.product.save()

        # Add tracking event
        OrderTracking.objects.create(
            order=order,
            status='Order Placed',
            description=f'Your order {order.order_number} has been placed successfully.',
            location='Online'
        )

        # Track activity
        UserActivity.objects.create(
            user=request.user, activity_type='purchase',
            metadata={'order_id': str(order.id), 'total': str(total)}
        )

        # Clear cart
        cart.items.all().delete()

        # Redirect to payment
        return redirect('payment_process', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart, 'items': items, 'addresses': addresses,
    })


@login_required
def order_list(request):
    """User's order history."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail page."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    items = order.items.select_related('product').all()
    tracking = order.tracking_events.all()
    return render(request, 'orders/order_detail.html', {
        'order': order, 'items': items, 'tracking': tracking,
    })


@login_required
def track_order(request, order_id):
    """Order tracking page with timeline."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    tracking = order.tracking_events.all()
    return render(request, 'orders/tracking.html', {
        'order': order, 'tracking': tracking,
    })
