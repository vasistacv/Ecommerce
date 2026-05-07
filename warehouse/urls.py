"""Warehouse URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.warehouse_dashboard, name='warehouse_dashboard'),
]
