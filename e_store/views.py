from django.shortcuts import render, redirect, reverse
from rest_framework import status
from e_store.models import Product, Address, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from .api.serializers import ProductSerializer, OrderSerializer
from accounts.forms import AddressForm, OrderForm
from django.forms import inlineformset_factory, modelformset_factory
from accounts.models import User
from django.contrib import messages
from e_store.utils import pay_choice_converter, create_orderitems, create_transaction_id
# Create your views here.


def store_view(request):
    success = messages.get_messages(request)
    search = request.GET.get('name')
    if search != None:
        obj = Product.objects.filter(name__icontains=search)
    else:
        obj = Product.objects.all()
    context = {
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
@parser_classes([JSONParser])
def cart_ajax_handler(request):
    if request.method == 'GET':
        print(request.query_params)
        prod_code = request.query_params.get('code')
        if prod_code == None:
            raise Exception('prod_code is None')
        print(prod_code)
        try:
            obj = Product.objects.get(code=prod_code)
        except Product.DoesNotExist:
            return Response(status=404)
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
            if (user.addresses.all().exists()):
                address = request.user.addresses.all().get(current=True)
                context = {
                    'address' : address
                }
            else:
                messages.warning(request, 'Please set an address first')
                return redirect('store:set_address')
    else:
        messages.warning(request, 'Please login first')
        return redirect('accounts:login')      
    return render(request, 'e_store/checkout.html', context)


@api_view(['POST'])
@parser_classes([JSONParser])
def placeorder_ajax(request, format=None):
    user = request.user
    if request.method == 'POST':
        payment = request.data.get('payment')
        if payment == None:
            raise Exception("Sorry, payment variable is None.")
        address = request.user.addresses.all().get(current=True)
        data = {
            'name' : address.name,
            'mobile' : address.mobile,
            'transaction_id' : create_transaction_id(),
            'ship_address' : address.get_complete_address,
            'payment_type' : pay_choice_converter(payment),
        }
        form = OrderForm(data)
        if form.is_valid():
            items = request.data.get('products')
            if items == None:
                raise Exception("Sorry, items variable is None.")
            order = form.save(commit=False)
            order.customer = user
            order.save()
            create_orderitems(order, items)
            obj = Order.objects.get(transaction_id=order.transaction_id)
            serializer = OrderSerializer(obj)
            if request.is_ajax():
                return Response(serializer.data, status=200)
        else:
            return Response(form.errors.as_json(), status=500)
            


@api_view(['GET'])
@parser_classes([JSONParser])
def autocomplete_ajax(request):
    if request.method == 'GET':
        input = request.query_params.get('input')
        if input == None:
            raise Exception("input is None")
        print(input)
        try:
            obj = Product.objects.filter(name__icontains=input)[:5]
        except Product.DoesNotExist:
            return Response(status=404)
        serializer = ProductSerializer(obj, many=True)
        if request.is_ajax():
            return Response(serializer.data, status=200)
    else:
        return Response(status=405)
