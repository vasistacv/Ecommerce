"""Product URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/review/', views.submit_review, name='submit_review'),
]
