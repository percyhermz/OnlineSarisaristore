from django.urls import path, include
from e_store import views


app_name='store'


urlpatterns = [
    path('', views.store_view, name="store_view"),
    path('detail/<str:code>', views.product_detail_view, name="product_detail"),
    path('add_to_cart/', views.cart_ajax_handler, name="ajax_add_to_cart"),
    path('set_address/', views.set_address_view, name="set_address"),
    path('checkout/', views.checkout_view, name="checkout"),
    path('checkout/placeorder/', views.placeorder_ajax, name='ajax_placeorder')
]
