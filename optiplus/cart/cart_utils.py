# cart/cart_utils.py
from .models import Cart

def get_cart_data(request):
    """Helper function to get cart data for context processor"""
    cart = None
    cart_items = []
    total = 0
    item_count = 0

    try:
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Get or create cart for logged in user
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.select_related('product', 'product__brand').all()
        else:
            # Get cart from session
            cart_id = request.session.get('cart_id')
            if cart_id:
                try:
                    cart = Cart.objects.get(id=cart_id)
                    cart_items = cart.items.select_related('product', 'product__brand').all()
                except Cart.DoesNotExist:
                    cart = None

        # Calculate totals
        if cart:
            total = cart.get_total()
            item_count = cart.get_items_count()
    except Exception:
        # Handle any potential errors gracefully
        pass

    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': total,
        'cart_count': item_count
    }