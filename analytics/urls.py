"""Analytics URL patterns."""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='analytics_dashboard'),
    path('api/revenue/', views.revenue_data, name='revenue_data'),
]
