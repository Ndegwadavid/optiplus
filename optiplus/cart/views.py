# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from products.models import EyewearProduct
from .models import Cart, CartItem

def get_or_create_cart(request):
    """Helper function to get or create a cart based on user authentication status"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
        else:
            cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

def cart_detail(request):
    """Display cart contents and total"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'product__brand').all()

    subtotal = sum(item.get_total() for item in cart_items)
    # You can add tax calculation and shipping cost here
    total = subtotal

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_html = render_to_string('cart/includes/cart_items.html', context, request)
        return JsonResponse({
            'cart_html': cart_html,
            'total': total,
            'item_count': cart.get_items_count()
        })
        
    return render(request, 'cart/cart_detail.html', context)

@require_POST
def add_to_cart(request, product_id):
    """Add a product to cart with specified quantity"""
    cart = get_or_create_cart(request)
    product = get_object_or_404(EyewearProduct, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': cart.get_items_count(),
            'cart_total': cart.get_total()
        })

    messages.success(request, f'{product.name} added to cart')
    return redirect('cart:cart_detail')

@require_POST
def update_cart(request, item_id):
    """Update the quantity of a cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 0))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        message = 'Cart updated successfully'
    else:
        cart_item.delete()
        message = 'Item removed from cart'

    cart = cart_item.cart
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.get_total(),
            'item_total': cart_item.get_total() if quantity > 0 else 0,
            'cart_count': cart.get_items_count()
        })

    messages.success(request, message)
    return redirect('cart:cart_detail')

@require_POST
def remove_from_cart(request, item_id):
    """Remove an item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_total': cart.get_total(),
            'cart_count': cart.get_items_count()
        })

    messages.success(request, 'Item removed from cart')
    return redirect('cart:cart_detail')

@require_POST
def clear_cart(request):
    """Remove all items from cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
            'cart_total': 0,
            'cart_count': 0
        })

    messages.success(request, 'Cart cleared')
    return redirect('cart:cart_detail')

# Optional: Cart merging when user logs in
def merge_carts(user_cart, session_cart):
    """Merge anonymous cart with user cart when logging in"""
    if not session_cart or user_cart == session_cart:
        return
    
    for item in session_cart.items.all():
        try:
            user_item = CartItem.objects.get(
                cart=user_cart,
                product=item.product
            )
            user_item.quantity += item.quantity
            user_item.save()
        except CartItem.DoesNotExist:
            item.cart = user_cart
            item.save()
    
    session_cart.delete()