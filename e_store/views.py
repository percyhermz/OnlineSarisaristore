from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
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

