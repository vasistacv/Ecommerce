"""Warehouse dashboard views."""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F, Q
from .models import Warehouse, Inventory, Shipment
from products.models import Product
from orders.models import Order


@staff_member_required
def warehouse_dashboard(request):
    """Warehouse management dashboard."""
    warehouses = Warehouse.objects.filter(is_active=True)

    # Total stats
    total_inventory = Inventory.objects.aggregate(
        total=Sum('quantity'),
        reserved=Sum('reserved')
    )

    # Low stock alerts
    low_stock_items = Inventory.objects.filter(
        quantity__lte=F('reorder_level')
    ).select_related('product', 'warehouse').order_by('quantity')[:20]

    # Pending shipments
    pending_shipments = Shipment.objects.filter(
        status__in=['preparing', 'packed']
    ).select_related('order', 'warehouse').order_by('created_at')[:15]

    # Active shipments
    active_shipments = Shipment.objects.filter(
        status__in=['dispatched', 'in_transit']
    ).select_related('order', 'warehouse').order_by('-shipped_at')[:10]

    # Orders awaiting fulfillment
    awaiting_fulfillment = Order.objects.filter(
        status__in=['confirmed', 'processing']
    ).select_related('user').order_by('created_at')[:10]

    # Products with critically low stock
    critical_stock = Product.objects.filter(
        stock__lte=F('min_stock_alert'), is_active=True
    ).order_by('stock')[:10]

    context = {
        'warehouses': warehouses,
        'total_inventory': total_inventory.get('total') or 0,
        'total_reserved': total_inventory.get('reserved') or 0,
        'low_stock_items': low_stock_items,
        'pending_shipments': pending_shipments,
        'active_shipments': active_shipments,
        'awaiting_fulfillment': awaiting_fulfillment,
        'critical_stock': critical_stock,
    }
    return render(request, 'warehouse/dashboard.html', context)
