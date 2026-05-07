from django.contrib import admin
from .models import Warehouse, Inventory, Shipment

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'city', 'capacity', 'current_occupancy', 'occupancy_percent', 'is_active']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'reserved', 'available', 'needs_reorder']
    list_filter = ['warehouse']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'warehouse', 'status', 'carrier', 'tracking_number', 'created_at']
    list_filter = ['status', 'warehouse']
