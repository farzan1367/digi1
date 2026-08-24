from django.contrib import admin
from django.utils.html import format_html

from . import models
from django.contrib.auth.models import User

from .models import Category, Brand, Product,ProductMedia

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

class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    list_display = ['file']
    extra = 0

    readonly_fields = ['media_preview']

    class Media:
        js = ('shop/js/product_media_preview.js',)

    def media_preview(self, obj):
        if not obj.file:
            return ''
        elif obj.media_type=='image':
            return format_html(
                '<img src="{url}" width="100" height="100" style="object-fit:cover;"/>',
                url = obj.file.url
            )
        elif obj.media_type=='video':
            return format_html(
                '<video  width="100" height="100" controls>'
                '<source src="{url}">'
                '</video>',
                url = obj.file.url

            )
        return ''

    media_preview.short_description = 'Preview'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','brand','category','price','is_sale']
    list_filter = ['brand','category','is_sale']
    search_fields = ['name']
    inlines = [ProductMediaInline]


