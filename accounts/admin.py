from django.contrib import admin
from accounts.models import User
from e_store.models import Address
# Register your models here.

class AddressInline(admin.StackedInline):
        model = Address
        extra = 0


class UserAdmin(admin.ModelAdmin):
        model = User
        inlines = [
            AddressInline,
        ]
        fields = ['username', 'email', 'first_name', 'last_name', 'mobile', 'is_admin', 'password']

class AddressAdmin(admin.ModelAdmin):
    class Meta:
        model = Address
        fields = ['detailed_address', 'mobile', 'name']


admin.site.register(User, UserAdmin)
