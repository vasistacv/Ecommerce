"""Order models - orders, items, tracking."""
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import Address
import uuid
import random
import string


def generate_order_number():
    prefix = 'ORD'
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=8))
    return f"{prefix}-{suffix}"


class Order(models.Model):
    """Customer order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Address
    shipping_name = models.CharField(max_length=150)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    shipping_phone = models.CharField(max_length=20)

    # Pricing
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # AI Fraud Detection
    fraud_score = models.FloatField(null=True, blank=True, help_text='0-1 fraud risk score')
    fraud_flagged = models.BooleanField(default=False)
    fraud_reason = models.TextField(blank=True)

    notes = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"

    @property
    def status_percentage(self):
        status_map = {
            'pending': 10, 'confirmed': 20, 'processing': 35,
            'shipped': 50, 'in_transit': 70, 'out_for_delivery': 90,
            'delivered': 100, 'cancelled': 0, 'returned': 0, 'refunded': 0,
        }
        return status_map.get(self.status, 0)


class OrderItem(models.Model):
    """Individual item within an order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)
    product_sku = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"


class OrderTracking(models.Model):
    """Order tracking history events."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_events')
    status = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_tracking'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"
