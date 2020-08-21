from django.shortcuts import render, redirect, reverse
from rest_framework import status
from .models import Product, Address, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .api.serializers import ProductSerializer
from accounts.forms import AddressForm
from django.forms import inlineformset_factory, modelformset_factory
from accounts.models import User
from django.contrib import messages
# Create your views here.

def store_view(request):
    success = messages.get_messages(request)
    obj = Product.objects.all()
    context = {
        'multiplier' : range(12),
        'obj' : obj,
        'messages': success
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
        


def set_address_view(request):
    user = request.user
    context = {}
    context['messages'] = messages.get_messages(request)
    if user.is_authenticated:
        if request.POST:
            form = AddressForm(request.POST)
            if form.is_valid:
                profile = form.save(commit=False)
                profile.customer = request.user
                profile.save()
                messages.success(request, 'Address added successfullly')
                return redirect('store:store_view')
            else:
                form = AddressForm(request.POST)
                context['ship_form'] = ship_form
        else:
            ship_form = AddressForm()
            context['ship_form'] = ship_form
    else:
        messages.warning(request, 'Please login first')
        return redirect('accounts:login')
    return render(request, 'e_store/set_address.html', context)



def checkout_view(request):
    user = request.user
    if user.is_authenticated:
        if request.POST:
            form = request.POST
        else:# GET Method
            if (user.addresses.all().exists()):
                address = request.user.addresses.all().get(current=True)
                name = address.name
                context = {
                    'name' : name,
                    'address': address,
                }
            else:
                messages.warning(request, 'Please set an address first')
                return redirect('store:set_address')
    else:
        messages.warning(request, 'Please login first')
        return redirect('accounts:login')      
    return render(request, 'e_store/checkout.html', context)
