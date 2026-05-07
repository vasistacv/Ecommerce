"""Root URL Configuration for Smart E-Commerce Platform."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from products.models import Product, Category
        context['featured_products'] = Product.objects.filter(is_featured=True, is_active=True)[:8]
        context['categories'] = Category.objects.filter(is_active=True)[:8]
        context['latest_products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
        context['deals'] = Product.objects.filter(discount_percent__gt=0, is_active=True).order_by('-discount_percent')[:4]
        return context


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('api/ai/', include('ai_engine.urls')),
    path('analytics/', include('analytics.urls')),
    path('warehouse/', include('warehouse.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
