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
    slug = models.CharField(max_length=255,blank=True)
    parent = models.ForeignKey('self', null=True, blank=True,related_name='children',on_delete=models.CASCADE)
    # is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.slug = self.slug.replace("-","")
        super().save(*args, **kwargs)
        
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone=models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password=models.CharField(max_length=20)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
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

class Brand(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/',blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    name = models.CharField(max_length=300)
    # slug = models.SlugField(unique=True)
    description= models.TextField()
    # is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    price=models.DecimalField(max_digits=20,decimal_places=0,default="0")
    picture=models.ImageField(upload_to='upload/product/')

    star=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(decimal_places=0,max_digits=20,default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer=models.ForeignKey(Customer ,on_delete=models.CASCADE)
    product=models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantitiy=models.IntegerField(default=1)
    adress=models.CharField(max_length=500,default="",blank=False)
    phone=models.CharField(max_length=20,blank=True)
    date=models.DateField(default=datetime.now)
    statuse=models.BooleanField(default=False)


    def __str__(self):
        return   self.product      