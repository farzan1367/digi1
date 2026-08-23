from django.contrib import admin
from . import models
from django.contrib.auth.models import User

from .models import Category, Brand, Product

admin.site.register(models.Category)
# admin.site.register(models.Product)
# admin.site.register(models.Brand)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.Profile)


class ProfileInLine(admin.StackedInline):
    model = models.Profile

class UserAdmin(admin.ModelAdmin): 
    model = User
    fields = ['username','first_name','last_name','email']
    inlines =[ProfileInLine]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','slug','is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','brand','category','price','is_sale']
    list_filter = ['brand','category','is_sale']
    search_fields = ['name']

