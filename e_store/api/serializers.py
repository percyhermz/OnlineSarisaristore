from rest_framework import serializers
from e_store.models import Product, Images, Order



class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['num', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    # image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Product
        fields = ['name', 'price', 'code', 'category', 'images']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['transaction_id', 'payment_type', 'name', 'mobile']
