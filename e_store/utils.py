from accounts.forms import OrderItemForm
from e_store.models import Order, Product
import random
import string as str_func
from datetime import date



def pay_choice_converter(method):
    switch = {
        'COD' : Order.PayChoices.COD,
        'Gcash' : Order.PayChoices.GCASH,
        'PayMaya' : Order.PayChoices.PAYMAYA,
        'Bank' : Order.PayChoices.BANK,
    }
    return switch.get(method, Order.PayChoices.COD)


def create_orderitems(Order_object, products):
    order_obj = Order_object
    for items in products:
        data = {
            'total_price' : products[items]['total_price'],
            'quantity' : products[items]['quantity'],
            'product' : Product.objects.get(code=products[items]['code']),
        }
        form = OrderItemForm(data)
        if form.is_valid:
            orderitem = form.save(commit=False)
            orderitem.order = order_obj
            orderitem.save()


def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(str_func.ascii_lowercase + str_func.ascii_uppercase + str_func.digits)
	return key


def create_transaction_id():
    key = random_key(16)
    now = date.today().strftime('%d%m%y')
    transact_id = now + key
    return transact_id