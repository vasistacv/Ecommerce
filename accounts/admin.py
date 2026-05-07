from django.contrib import admin
from .models import UserProfile, Address, UserActivity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'loyalty_points', 'is_premium', 'created_at']
    list_filter = ['is_premium']
    search_fields = ['user__username', 'user__email', 'phone']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'state', 'address_type', 'is_default']
    list_filter = ['address_type', 'is_default']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'product', 'timestamp']
    list_filter = ['activity_type']
