"""Product views - listing, detail, search, review submission."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Product, Category, Review
from accounts.models import UserActivity


def product_list(request):
    """Product listing with filters, search, and sorting."""
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    # Filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand__iexact=brand)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    rating = request.GET.get('rating')
    if rating:
        products = products.filter(avg_rating__gte=rating)

    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(stock__gt=0)

    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(tags__icontains=query)
        )
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user, activity_type='search', search_query=query
            )

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    sort_options = {
        'price_low': 'price',
        'price_high': '-price',
        'rating': '-avg_rating',
        'newest': '-created_at',
        'popular': '-total_sold',
        'name': 'name',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    # Get unique brands for filter
    brands = Product.objects.filter(is_active=True).values_list('brand', flat=True).distinct().order_by('brand')

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)

    context = {
        'products': products,
        'categories': categories,
        'brands': [b for b in brands if b],
        'query': query,
        'current_category': category_slug,
        'current_sort': sort,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    """Product detail page with reviews and recommendations."""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Increment view count
    Product.objects.filter(pk=product.pk).update(views_count=models.F('views_count') + 1)

    # Track activity
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user, activity_type='view', product=product
        )

    reviews = product.reviews.filter(is_approved=True).select_related('user')
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    # Price history for chart
    price_history = product.price_history.all()[:30]

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'price_history': list(price_history.values('price', 'recorded_at')),
    }
    return render(request, 'products/detail.html', context)


# Need this import for F expression
from django.db import models


@login_required
def submit_review(request, slug):
    """Submit a product review."""
    product = get_object_or_404(Product, slug=slug)

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('product_detail', slug=slug)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        pros = request.POST.get('pros', '')
        cons = request.POST.get('cons', '')

        review = Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            title=title,
            content=content,
            pros=pros,
            cons=cons,
        )

        # Track activity
        UserActivity.objects.create(
            user=request.user, activity_type='review', product=product,
            metadata={'rating': rating}
        )

        messages.success(request, 'Your review has been submitted! ✅')
        return redirect('product_detail', slug=slug)

    return redirect('product_detail', slug=slug)
