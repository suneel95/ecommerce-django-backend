"""
Function-based views only. Each view does one job - easy to follow.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import RegisterForm


# ----- Home -----
def home(request):
    """Landing page: show a few featured products and welcome message."""
    products = Product.objects.all()[:6]
    return render(request, 'store/home.html', {'products': products})


# ----- Product listing and detail -----
def product_list(request):
    """List all products."""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, slug):
    """Show one product and add-to-cart form."""
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


# ----- Auth: Register, Login, Logout -----
def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Welcome.')
            return redirect('store:home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next') or reverse('store:home')
            return redirect(next_url)
        messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    """Log user out and redirect to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:home')


# ----- Cart -----
def get_or_create_cart(user):
    """Helper: get user's cart or create one if it doesn't exist."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    """Display current cart and allow quantity updates."""
    cart = get_or_create_cart(request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    """Add one product to cart (or increase quantity). Redirect back to product or cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'Added {product.name} to cart.')
    # Redirect to next or product detail or cart
    next_url = request.GET.get('next', 'store:cart')
    return redirect(next_url)


@login_required
def update_cart_item(request, item_id):
    """Update quantity of a cart item. POST only."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    new_qty = request.POST.get('quantity')
    try:
        qty = int(new_qty)
        if qty <= 0:
            item.delete()
            messages.info(request, 'Item removed from cart.')
        else:
            item.quantity = min(qty, item.product.stock)
            item.save()
            messages.success(request, 'Cart updated.')
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity.')
    return redirect('store:cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove one item from cart."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('store:cart')


# ----- Checkout and orders -----
@login_required
def checkout(request):
    """Show checkout page with cart summary. POST = place order."""
    cart = get_or_create_cart(request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')
    if request.method == 'POST':
        with transaction.atomic():
            order = Order.objects.create(user=request.user, total=cart.total_price(), status='confirmed')
            for cart_item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order=order,
                    product_name=cart_item.product.name,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )
            cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('store:order_confirmation', order_id=order.id)
    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_confirmation(request, order_id):
    """Thank-you page after placing an order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    """List all orders for the current user."""
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Show details for a single order belonging to the current user."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
