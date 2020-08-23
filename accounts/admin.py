from django.contrib import admin
from accounts.models import User
from e_store.models import Address, Order
# Register your models here.

class AddressInline(admin.TabularInline):
        model = Address
        extra = 0

class OrderInline(admin.TabularInline):
        model = Order
        extra = 0

class UserAdmin(admin.ModelAdmin):
        model = User
        inlines = [
        AddressInline,
        OrderInline
        ]
        fields = ['username', 'email', 'first_name', 'last_name', 'mobile', 'is_admin', 'password']



admin.site.register(User, UserAdmin)
