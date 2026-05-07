"""Payment processing views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from orders.models import Order, OrderTracking
from .models import Payment
import uuid
import random
import string


def generate_transaction_id():
    return 'TXN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


@login_required
def payment_process(request, order_id):
    """Payment processing page."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if hasattr(order, 'payment') and order.payment.status == 'completed':
        messages.info(request, 'This order has already been paid.')
        return redirect('order_detail', order_id=order.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'card')
        card_number = request.POST.get('card_number', '')
        card_last_four = card_number[-4:] if len(card_number) >= 4 else '0000'

        # Simulate payment processing
        transaction_id = generate_transaction_id()

        # Determine card brand
        card_brand = 'Visa'
        if card_number.startswith('5'):
            card_brand = 'Mastercard'
        elif card_number.startswith('3'):
            card_brand = 'Amex'
        elif card_number.startswith('6'):
            card_brand = 'RuPay'

        payment = Payment.objects.create(
            order=order,
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status='completed',
            card_last_four=card_last_four,
            card_brand=card_brand if payment_method == 'card' else '',
            metadata={
                'payment_method': payment_method,
                'processed_at': str(timezone.now()),
            }
        )

        # Update order
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()

        # Add tracking event
        OrderTracking.objects.create(
            order=order,
            status='Payment Received',
            description=f'Payment of ₹{order.total} received via {payment.get_payment_method_display()}. Transaction ID: {transaction_id}',
            location='Payment Gateway'
        )

        # Add loyalty points
        profile = request.user.profile
        profile.loyalty_points += int(float(order.total) / 10)
        profile.save()

        messages.success(request, f'Payment successful! Transaction ID: {transaction_id} 🎉')
        return redirect('payment_success', order_id=order.id)

    return render(request, 'payments/payment.html', {'order': order})


@login_required
def payment_success(request, order_id):
    """Payment success page."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'payments/success.html', {'order': order})
