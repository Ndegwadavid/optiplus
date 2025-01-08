# products/admin.py
from django.contrib import admin
from .models import Brand, Category, EyewearProduct

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order']
    list_editable = ['display_order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(EyewearProduct)
class EyewearProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'category', 'sku', 'price', 
        'sale_price', 'in_stock', 'stock_qty', 'is_available'
    ]
    list_filter = ['brand', 'category', 'frame_shape', 'frame_material', 'is_available', 'in_stock']
    list_editable = ['price', 'sale_price', 'in_stock', 'stock_qty', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'sku', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('brand', 'category', 'name', 'slug', 'sku', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price')
        }),
        ('Images', {
            'fields': ('main_image', 'image_2', 'image_3')
        }),
        ('Frame Details', {
            'fields': ('frame_shape', 'frame_material', 'frame_width', 'lens_width', 
                      'bridge_width', 'temple_length')
        }),
        ('Stock Management', {
            'fields': ('is_available', 'in_stock', 'stock_qty')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        })
    )