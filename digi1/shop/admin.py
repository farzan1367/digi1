from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User

from . import models
from .models import Category, Brand, Product,ProductMedia,Inventory

admin.site.register(models.Category)
# admin.site.register(models.Product)
# admin.site.register(models.Brand)
# admin.site.register(models.Customer)
# admin.site.register(models.Order)
admin.site.register(models.Profile)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','reserved_quantity','available_quantity','low_stock_threshold','updated_at',]

    list_filter = ['quantity']

    search_fields = ['product__name']

    readonly_fields = ['available_quantity', 'updated_at']

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
    extra = 0
    can_delete = True

    ordering = ['sort_order']

    readonly_fields = [
        'media_preview',
        'media_actions',
    ]

    fields = [
        'media_preview',
        'file',
        'media_actions',
    ]

    class Media:
        js = ('shop/js/product_media_preview.js',)
        css = {
            'all': ('shop/css/product_media_admin.css',)
        }

    def media_preview(self, obj):
        if not obj.file:
            return ''

        elif obj.media_type == 'image':
            return format_html(
                '<img src="{url}" width="100" height="100" '
                'style="object-fit:cover;"/>',
                url=obj.file.url
            )

        elif obj.media_type == 'video':
            return format_html(
                '<video width="100" height="100" controls>'
                '<source src="{url}">'
                '</video>',
                url=obj.file.url
            )

        return ''

    media_preview.short_description = 'Preview'

    def media_actions(self, obj):
        if not obj.pk:
            return ''

        return format_html(
            '''
            <div class="media-actions">

                <button type="button"
                        class="media-drag-handle"
                        title="برای جابه‌جایی بکشید">
                    <span class="drag-icon">☷</span>
                    جابه‌جایی
                </button>

                <button type="button"
                        class="media-delete-button"
                        data-media-id="{}"
                        title="حذف این فایل">
                    <span class="delete-icon">🗑</span>
                    حذف
                </button>

            </div>
            ''',
            obj.pk
        )

    media_actions.short_description = 'Actions'

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0
    readonly_fields = ['available_quantity', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'is_sale']
    list_filter = ['brand', 'category', 'is_sale']
    search_fields = ['name']
    inlines = [ProductMediaInline, InventoryInline]
    change_form_template = 'admin/shop/product/change_form.html'