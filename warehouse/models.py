"""Warehouse models - warehouses, inventory, shipments."""
from django.db import models
from products.models import Product
import uuid


class Warehouse(models.Model):
    """Warehouse location."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    capacity = models.IntegerField(help_text='Total storage capacity in units')
    current_occupancy = models.IntegerField(default=0)
    manager_name = models.CharField(max_length=150, blank=True)
    manager_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'warehouses'

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def occupancy_percent(self):
        if self.capacity > 0:
            return round((self.current_occupancy / self.capacity) * 100, 1)
        return 0


class Inventory(models.Model):
    """Product inventory per warehouse."""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouse_inventory')
    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0, help_text='Reserved for pending orders')
    reorder_level = models.IntegerField(default=10)
    last_restocked = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'warehouse_inventory'
        unique_together = ['warehouse', 'product']

    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name}: {self.quantity}"

    @property
    def available(self):
        return self.quantity - self.reserved

    @property
    def needs_reorder(self):
        return self.available <= self.reorder_level


class Shipment(models.Model):
    """Shipment tracking for warehouse."""
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('packed', 'Packed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='shipments')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='shipments')
    tracking_number = models.CharField(max_length=100, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Shipment for {self.order.order_number}"
