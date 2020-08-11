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
        return reverse('product_detail', kwargs={'code' : self.code})

    def get_images(self):
        return self.images_set.all()

    def get_thumbnail(self):
        return self.images_set.get(num=1).image.url


class Images(models.Model):
    def get_image_num(self):
        pass


    num = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)








