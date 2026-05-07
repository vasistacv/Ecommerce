"""Payment URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path('process/<uuid:order_id>/', views.payment_process, name='payment_process'),
    path('success/<uuid:order_id>/', views.payment_success, name='payment_success'),
]
