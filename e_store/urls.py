from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.store_view, name="store_view"),
    path('detail/<str:code>', views.product_detail_view, name="product_detail")
]
