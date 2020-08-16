from django.shortcuts import render
from rest_framework import status
from .models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .api.serializers import ProductSerializer 
# Create your views here.

def store_view(request):
    obj = Product.objects.all()
    context = {
        'multiplier' : range(12),
        'obj' : obj,
    }
    return render(request, 'e_store/store.html', context)

def product_detail_view(request, code):
    obj = Product.objects.get(code=code)
    context = {
        "product" : obj,
    }
    return render(request, 'e_store/details.html', context)

@api_view(['GET'])
def cart_ajax_handler(request):
    if request.method == 'GET':
        prod_code = request.GET.get('code')
        try:
            obj = Product.objects.get(code=prod_code)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_RESPONSE_404)
        serializer =  ProductSerializer(obj)
        if request.is_ajax():
            return Response(serializer.data, status=200)
        
