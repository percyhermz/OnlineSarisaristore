from django.db import models
from django.shortcuts import reverse
# Create your models here.


class Product(models.Model):

    class ProductCategory(models.TextChoices):
        CANNED = 'Canned Goods', ('Canned Goods')
        NOODLES = 'Noodles', ('Noodles')
        VEGGIES = 'Vegetables', ('Vegetables')
        RICE = 'Rice', ('Rice')

    
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=ProductCategory.choices, default=ProductCategory.CANNED)
    price = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    def get_detail_url(self):
        return reverse('store:product_detail', kwargs={'code' : self.code})

    def get_images(self):
        return self.images.all()

    def get_thumbnail(self):
        return self.images.get(num=1).image.url


class Images(models.Model):
    num = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)


class Order(models.Model):

    class PayChoices(models.TextChoices):
        COD = 'Cash on Delivery', ('Cash on Delivery')
        PAYMAYA = 'PayMaya', ('PayMaya')
        GCASH = 'Gcash', ('Gcash')
        BANK = 'Bank', ('Bank')


    customer = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    ship_address = models.CharField(max_length=100, verbose_name="Delivered to", default="address") 
    payment_type = models.CharField(max_length=20, choices=PayChoices.choices, default=PayChoices.COD,verbose_name="Payment Method")
    name = models.CharField(max_length=40, verbose_name="Name", default='Name')
    mobile = models.CharField(max_length=11, verbose_name="Mobile No.", default='09') 
 

    def __str__(self):
        return str(self.name) + " " + self.mobile

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    @property
    def get_total(self):
        return self.total_price
    

class Address(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='addresses')
    detailed_address = models.CharField(max_length=20, verbose_name="Detailed Address: House#/Buildingname/Street", default="address")
    brgy_dist_name = models.CharField(max_length=20, verbose_name="Barangay")
    city = models.CharField(max_length=20, verbose_name="City")
    region = models.CharField(max_length=20, verbose_name="Region", default="address")
    province = models.CharField(max_length=20, verbose_name="Province")
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code", default="postal_code here")
    name = models.CharField(max_length=20, verbose_name="Name", default="Please put your name")
    mobile = models.CharField(max_length=20, verbose_name="Mobile #", default="Please update your number")
    distance_to_store = models.IntegerField(default=0, verbose_name="Shipping Distance(km)")
    current = models.BooleanField(default=True)

    @property
    def get_est_fee(self):
        fee_per_km = 8
        initial_fee = 60
        additional_fee = initial_fee + int(round(self.distance_to_store))*fee_per_km
        default = 200
        return default

    @property
    def get_complete_address(self):
        address1 =  self.detailed_address + " " + self.brgy_dist_name
        address2 =  self.region + "~" + self.province
        address3 =  self.city + " " + self.postal_code
        address = address1 + " " + address2+ " " + address3
        return address

    @property
    def get_mobile(self):
        return self.mobile

    @property
    def get_name(self):
        return self.name

    def __str__(self):
        return "Owner: " + str(self.customer) + "Address: " + str(self.get_complete_address)


    

    




