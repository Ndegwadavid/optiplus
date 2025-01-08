# cart/context_processors.py
from .models import Cart

def cart_processor(request):
    cart = None
    cart_items = []
    total = 0
    item_count = 0

    try:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                try:
                    cart = Cart.objects.get(id=cart_id)
                except Cart.DoesNotExist:
                    cart = None

        if cart:
            cart_items = cart.items.select_related('product', 'product__brand').all()
            total = cart.get_total()
            item_count = cart.get_items_count()

    except Exception:
        pass

    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': total,
        'cart_count': item_count
    }