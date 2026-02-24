"""
Context processor: makes cart item count available in every template.
So the navbar can show "Cart (3)" without passing it from every view.
"""
def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart = getattr(request.user, 'cart', None)
        if cart:
            count = sum(item.quantity for item in cart.items.all())
    return {'cart_count': count}
