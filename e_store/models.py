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
    customer = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

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



class Address(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    h_b_st_number = models.CharField(max_length=20, verbose_name="House/Building/Street Number")
    st_name = models.CharField(max_length=20, verbose_name="Street Name")
    brgy_dist_name = models.CharField(max_length=20, verbose_name="Barangay/District Name")
    city = models.CharField(max_length=20, verbose_name="City/Municipality")
    province = models.CharField(max_length=20, verbose_name="Province")

