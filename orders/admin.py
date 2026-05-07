from django.contrib import admin
from .models import Order, OrderItem, OrderTracking

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']

class OrderTrackingInline(admin.TabularInline):
    model = OrderTracking
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total', 'fraud_flagged', 'created_at']
    list_filter = ['status', 'payment_status', 'fraud_flagged']
    search_fields = ['order_number', 'user__username']
    inlines = [OrderItemInline, OrderTrackingInline]
    readonly_fields = ['order_number']
