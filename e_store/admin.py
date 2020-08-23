from django.contrib import admin
from .models import Product, Images, Order, OrderItem


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

class OrderItemInline(admin.TabularInline):
        model = OrderItem
        extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    model = Order
      
    list_display = (
        'name',
        'mobile',
        'transaction_id',
        'date_ordered',
        'complete',
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)