"""Order URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('<uuid:order_id>/track/', views.track_order, name='track_order'),
]
