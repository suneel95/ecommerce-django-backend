"""
Admin configuration: add, edit, delete products from Django admin.
"""
from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug from name
    search_fields = ['name', 'description']


# Optional: view carts and orders in admin (read-only style)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status']


admin.site.register(CartItem)
admin.site.register(OrderItem)
