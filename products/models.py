"""Product catalog models - categories, products, reviews, price history."""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Category(models.Model):
    """Product category with hierarchical support."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class name (e.g., fas fa-laptop)')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_categories'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list') + f'?category={self.slug}'


class Product(models.Model):
    """Product model with comprehensive fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    min_stock_alert = models.IntegerField(default=5)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text='Weight in kg')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)
    total_sold = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def sale_price(self):
        if self.discount_percent > 0:
            return round(self.price * (1 - self.discount_percent / 100), 2)
        return self.price

    @property
    def savings(self):
        if self.discount_percent > 0:
            return round(self.price - self.sale_price, 2)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def low_stock(self):
        return 0 < self.stock <= self.min_stock_alert

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = reviews.count()
        else:
            self.avg_rating = 0
            self.total_reviews = 0
        self.save(update_fields=['avg_rating', 'total_reviews'])


class ProductImage(models.Model):
    """Additional product images."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_images'
        ordering = ['sort_order']


class Review(models.Model):
    """Product reviews with sentiment analysis support."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    helpful_count = models.IntegerField(default=0)
    # AI-generated fields
    sentiment_score = models.FloatField(null=True, blank=True, help_text='-1 to 1 sentiment score')
    sentiment_label = models.CharField(max_length=20, blank=True, help_text='positive/negative/neutral')
    is_fake = models.BooleanField(default=False, help_text='AI-detected fake review flag')
    fake_confidence = models.FloatField(null=True, blank=True, help_text='Confidence of fake detection')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_reviews'
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()


class PriceHistory(models.Model):
    """Track product price changes for price prediction."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_history'
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.product.name} - ₹{self.price} @ {self.recorded_at}"
