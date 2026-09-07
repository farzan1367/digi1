from time import sleep

from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255,blank=True)
    parent = models.ForeignKey('self', null=True, blank=True,related_name='children',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='categories/',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = self.slug.replace("-","")
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True,blank=True,null=True)
    sku = models.CharField(max_length=100,unique=True,null=True,blank=True)
    description= models.TextField()
    price=models.DecimalField(max_digits=20,decimal_places=0,default="0")
    sale_price = models.DecimalField(decimal_places=0, max_digits=20, default=0)
    picture=models.ImageField(upload_to='upload/product/')
    star=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    is_sale = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductMedia(models.Model):
    MEDIA_TYPE = (
        ('image','Image'),
        ('video','Video'),
    )
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='media')
    file = models.FileField(upload_to='upload/product/media/')
    media_type = models.CharField(max_length=10,choices=MEDIA_TYPE,editable=False)
    sort_order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.file:
            extension = self.file.name.lower().split('.')[-1]

            if extension in ['jpg','jpeg','png','webp','gif']:
                self.media_type = 'image'
            elif extension in ['mp4','webm','mov','avi']:
                self.media_type = 'video'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name

class Inventory(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='inventory',null=True,blank=True)
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_quantity(self):
        return max(self.quantity-self.reserved_quantity,0)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='specification')
    name = models.CharField(max_length=150)
    value = models.CharField(max_length=500)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['sort_order','id']

    def __str__(self):
        return f'{self.name}:{self.value}'






# class Customer(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     phone=models.CharField(max_length=20)
#     email = models.EmailField(max_length=100)
#     password=models.CharField(max_length=20)
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    date_modified=models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=25, blank=True)    
    adress1 = models.CharField(max_length=250, blank=True)    
    adress2 = models.CharField(max_length=250, blank=True) 
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zipcode = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=25, default='IRAN')  
    old_cart = models.CharField(max_length=200, blank=True, null=True) 
    
    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
# post_save.connect(create_profile,sender=User)










# class Order(models.Model):
#     customer=models.ForeignKey(Customer ,on_delete=models.CASCADE)
#     product=models.ForeignKey(Product ,on_delete=models.CASCADE)
#     quantitiy=models.IntegerField(default=1)
#     adress=models.CharField(max_length=500,default="",blank=False)
#     phone=models.CharField(max_length=20,blank=True)
#     date=models.DateField(default=datetime.now)
#     statuse=models.BooleanField(default=False)
#
#
#     def __str__(self):
#         return   self.product.name