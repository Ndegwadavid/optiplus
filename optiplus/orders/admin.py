# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product_name', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 
                   'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'id']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_per_page = 20
    ordering = ['-created_at']

    fieldsets = (
        ('Customer Information', {
            'fields': (
                'user', 'first_name', 'last_name', 'email', 'phone'
            )
        }),
        ('Order Information', {
            'fields': (
                'total_amount', 'status', 'order_notes'
            )
        }),
        ('Shipping Information', {
            'fields': (
                'address', 'city', 'postal_code'
            )
        }),
        ('Tracking', {
            'fields': (
                'tracking_number', 'created_at', 'updated_at'
            )
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'product_name', 'quantity', 'price']
    search_fields = ['order__id', 'product__name', 'product_name']
    list_filter = ['order__status']
    raw_id_fields = ['order', 'product']