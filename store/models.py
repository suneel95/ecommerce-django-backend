"""
Models for the store: Product, Cart, CartItem, Order, OrderItem.
Simple structure - easy to understand and explain in interviews.
"""
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """A product that can be sold. Managed via Django admin."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # For clean URLs, e.g. /product/blue-tshirt/
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Cart(models.Model):
    """One cart per user. Holds cart items until checkout."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        """Sum of all line items in this cart."""
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    """One product + quantity in a cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'product']  # One row per product per cart

    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """An order placed by a user. Contains order items and status."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # Simple status for display
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    """One product + quantity in an order (snapshot at time of order)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)  # Snapshot name
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.price * self.quantity
