from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_admin', 'mobile', 'email')
    fields = ['username', 'email', 'first_name', 'last_name', 'mobile', 'is_admin']
    


admin.site.register(User, UserAdmin)

