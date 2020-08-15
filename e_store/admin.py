from django.contrib import admin
from .models import Product, Images


# Register your models here.


class ImageInline(admin.TabularInline):
    model = Images

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = (
        'name',
        'code',
        'category'
    )


admin.site.register(Product, ProductAdmin)