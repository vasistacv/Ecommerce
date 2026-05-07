"""Management command to seed the database with sample data."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Review, PriceHistory
from warehouse.models import Warehouse, Inventory
from accounts.models import Address
from decimal import Decimal
import random
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed database with sample e-commerce data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@smartshop.com', 'admin123', first_name='Admin', last_name='User')
            self.stdout.write(self.style.SUCCESS('  [OK] Superuser created (admin/admin123)'))

        # Create test users
        users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={'email': f'user{i}@smartshop.com', 'first_name': f'User', 'last_name': f'{i}'}
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS('  [OK] Test users created'))

        # Categories
        categories_data = [
            ('Electronics', 'electronics', 'laptop'),
            ('Fashion', 'fashion', 'dress'),
            ('Home & Kitchen', 'home-kitchen', 'home'),
            ('Books', 'books', 'book'),
            ('Sports & Fitness', 'sports-fitness', 'sports'),
            ('Beauty & Health', 'beauty-health', 'beauty'),
            ('Toys & Games', 'toys-games', 'games'),
            ('Groceries', 'groceries', 'cart'),
        ]
        categories = []
        for name, slug, icon in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, slug=slug, defaults={'icon': icon})
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS('  [OK] Categories created'))

        # Products
        products_data = [
            ('MacBook Pro 16" M3 Max', 'macbook-pro-16-m3', 'SKU-EL-001', 'The most powerful MacBook ever with M3 Max chip, 36GB RAM, 1TB SSD. Stunning Liquid Retina XDR display.', categories[0], 'Apple', 249999, 10, True, 8),
            ('iPhone 15 Pro Max', 'iphone-15-pro-max', 'SKU-EL-002', 'A17 Pro chip. Titanium design. 48MP camera system. All-day battery life.', categories[0], 'Apple', 159999, 15, True, 12),
            ('Sony WH-1000XM5 Headphones', 'sony-wh1000xm5', 'SKU-EL-003', 'Industry-leading noise cancellation. 30-hour battery. Crystal clear calls.', categories[0], 'Sony', 29999, 20, True, 15),
            ('Samsung Galaxy S24 Ultra', 'samsung-s24-ultra', 'SKU-EL-004', 'Galaxy AI built in. 200MP camera. Titanium frame. S Pen included.', categories[0], 'Samsung', 134999, 10, False, 18),
            ('Dell XPS 15 Laptop', 'dell-xps-15', 'SKU-EL-005', 'Intel i9, 32GB RAM, OLED display. Ultra-slim design for professionals.', categories[0], 'Dell', 189999, 12, False, 20),
            ('Nike Air Max 270', 'nike-air-max-270', 'SKU-FA-001', 'The Nike Air Max 270 delivers visible cushioning under every step.', categories[1], 'Nike', 12999, 0, True, 25),
            ('Levis 501 Original Jeans', 'levis-501-jeans', 'SKU-FA-002', 'The original riveted jean since 1873. Straight fit, button fly.', categories[1], 'Levis', 4999, 5, False, 30),
            ('Ray-Ban Aviator Sunglasses', 'rayban-aviator', 'SKU-FA-003', 'Classic aviator shape in gold metal with green G-15 lenses.', categories[1], 'Ray-Ban', 8999, 10, True, 22),
            ('Dyson V15 Detect Vacuum', 'dyson-v15-detect', 'SKU-HK-001', 'Reveals microscopic dust with a laser. Most powerful suction.', categories[2], 'Dyson', 54999, 5, True, 12),
            ('Instant Pot Duo Plus', 'instant-pot-duo-plus', 'SKU-HK-002', '9-in-1 pressure cooker, sterilizer. Cooks up to 70% faster.', categories[2], 'Instant Pot', 9999, 0, False, 35),
            ('The Psychology of Money', 'psychology-of-money', 'SKU-BK-001', 'Timeless lessons on wealth, greed, and happiness by Morgan Housel.', categories[3], 'HarperCollins', 399, 0, True, 100),
            ('Atomic Habits', 'atomic-habits', 'SKU-BK-002', 'An easy & proven way to build good habits by James Clear.', categories[3], 'Penguin', 499, 0, True, 85),
            ('Yoga Mat Premium 6mm', 'yoga-mat-premium', 'SKU-SP-001', 'Extra thick, non-slip yoga mat with carrying strap.', categories[4], 'Boldfit', 1299, 0, False, 45),
            ('Fitbit Charge 6', 'fitbit-charge-6', 'SKU-SP-002', 'Advanced fitness tracker with stress management and GPS.', categories[4], 'Fitbit', 14999, 8, True, 20),
            ('Cetaphil Gentle Cleanser 500ml', 'cetaphil-cleanser', 'SKU-BH-001', 'Gentle skin cleanser for all skin types. Dermatologist recommended.', categories[5], 'Cetaphil', 899, 0, False, 60),
            ('PlayStation 5 DualSense Controller', 'ps5-dualsense', 'SKU-TG-001', 'Haptic feedback and adaptive triggers. Wireless Bluetooth controller.', categories[6], 'Sony', 5999, 0, True, 40),
        ]

        products = []
        for name, slug, sku, desc, cat, brand, price, disc, feat, stock in products_data:
            prod, _ = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name, 'sku': sku, 'description': desc, 'short_description': desc[:150],
                    'category': cat, 'brand': brand, 'price': Decimal(str(price)),
                    'cost_price': Decimal(str(int(price * 0.6))),
                    'discount_percent': Decimal(str(disc)), 'stock': stock,
                    'is_featured': feat, 'is_active': True,
                    'tags': f'{cat.name},{brand},trending',
                    'avg_rating': round(random.uniform(3.5, 5.0), 2),
                    'total_reviews': random.randint(5, 50),
                    'total_sold': random.randint(10, 200),
                }
            )
            products.append(prod)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(products)} products created'))

        # Reviews
        review_data = [
            ('Amazing product!', 'Absolutely love this product. Quality is top-notch and delivery was fast.', 5, 'Great quality', 'None'),
            ('Good value', 'Works well for the price. Would recommend to others.', 4, 'Affordable, functional', 'Packaging could improve'),
            ('Decent but overpriced', 'The product is okay but I expected more for this price point.', 3, 'Works as described', 'Expensive for features'),
            ('Excellent purchase', 'This exceeded my expectations. The build quality is premium.', 5, 'Premium feel, fast delivery', 'Nothing major'),
            ('Worth every penny', 'One of the best purchases I made. Highly recommended!', 5, 'Outstanding quality', 'Wish it came in more colors'),
        ]
        for prod in products[:8]:
            for i, (title, content, rating, pros, cons) in enumerate(review_data[:random.randint(2, 5)]):
                user = users[i % len(users)]
                Review.objects.get_or_create(
                    product=prod, user=user,
                    defaults={'title': title, 'content': content, 'rating': rating, 'pros': pros, 'cons': cons}
                )
        self.stdout.write(self.style.SUCCESS('  [OK] Reviews created'))

        # Price History
        for prod in products:
            base = float(prod.price)
            for day in range(30, 0, -1):
                PriceHistory.objects.get_or_create(
                    product=prod,
                    recorded_at=timezone.now() - timedelta(days=day),
                    defaults={'price': Decimal(str(round(base * random.uniform(0.92, 1.08), 2)))}
                )
        self.stdout.write(self.style.SUCCESS('  [OK] Price history created'))

        # Warehouses
        wh_data = [
            ('Mumbai Central', 'WH-MUM', 'Mumbai', 'Maharashtra', 5000, 3200),
            ('Delhi Hub', 'WH-DEL', 'New Delhi', 'Delhi', 8000, 5600),
            ('Bangalore Tech', 'WH-BLR', 'Bangalore', 'Karnataka', 3000, 1800),
        ]
        warehouses = []
        for name, code, city, state, cap, occ in wh_data:
            wh, _ = Warehouse.objects.get_or_create(
                code=code,
                defaults={'name': name, 'address': f'{city} Warehouse Zone', 'city': city, 'state': state, 'capacity': cap, 'current_occupancy': occ}
            )
            warehouses.append(wh)

        # Inventory
        for wh in warehouses:
            for prod in products:
                Inventory.objects.get_or_create(
                    warehouse=wh, product=prod,
                    defaults={'quantity': random.randint(5, 50), 'reserved': random.randint(0, 5)}
                )
        self.stdout.write(self.style.SUCCESS('  [OK] Warehouses & inventory created'))

        # Addresses for test users
        for user in users:
            Address.objects.get_or_create(
                user=user, is_default=True,
                defaults={
                    'full_name': f'{user.first_name} {user.last_name}',
                    'street_address': '123 Main Street', 'city': 'Mumbai',
                    'state': 'Maharashtra', 'zip_code': '400001',
                    'country': 'India', 'phone': '9876543210'
                }
            )
        self.stdout.write(self.style.SUCCESS('  [OK] Addresses created'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Admin Login: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('   Test User:   user1 / password123'))
