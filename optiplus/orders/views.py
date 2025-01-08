# orders/views.py
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart
from .forms import OrderForm

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total()
            
            # Set payment method from form
            payment_method = request.POST.get('payment_method', 'mpesa')
            order.payment_method = payment_method
            order.payment_status = 'pending'
            
            # Save order to generate order_id
            order.save()

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.sale_price or cart_item.product.price,
                    quantity=cart_item.quantity,
                    product_name=cart_item.product.name
                )

            # Clear the cart
            cart.items.all().delete()

            # Send confirmation email
            try:
                order.send_order_confirmation_email()
            except Exception as e:
                # Log the error but don't stop the order process
                print(f"Error sending email: {e}")
                messages.warning(
                    request, 
                    'Order placed successfully but there was an issue sending the confirmation email. '
                    'Please check your order details in your account.'
                )
            else:
                messages.success(
                    request, 
                    f'Order placed successfully! Order ID: {order.order_id}. '
                    'A confirmation email has been sent to your email address.'
                )

            # If payment method is M-Pesa, redirect to M-Pesa payment page
            if payment_method == 'mpesa':
                return redirect('orders:mpesa_payment', order_id=order.order_id)
            
            return redirect('orders:order_confirmation', order_id=order.order_id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'email': request.user.email,
            'phone': request.user.phone_number,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = OrderForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'payment_methods': Order.PAYMENT_METHOD,  # Add available payment methods to context
        'total_amount': cart.get_total(),
        'shipping_cost': 0,  # You can modify this based on your shipping logic
    }

    return render(request, 'orders/checkout.html', context)

#### mpesa integration:
@login_required
def mpesa_payment(request, order_id):
    """Handle M-Pesa payment process"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Here you would implement the actual M-Pesa payment integration
        # For now, we'll just simulate a successful payment
        phone_number = request.POST.get('phone_number')
        
        # Simulate successful payment
        order.payment_status = 'completed'
        order.mpesa_transaction_id = f'SIMULATED-{uuid.uuid4().hex[:8].upper()}'
        order.status = 'processing'
        order.save()
        
        messages.success(request, 'Payment processed successfully!')
        return redirect('orders:order_confirmation', order_id=order.order_id)
    
    context = {
        'order': order,
        'phone_number': order.phone  # Pre-fill with order phone number
    }
    return render(request, 'orders/mpesa_payment.html', context)

@login_required
def order_confirmation(request, order_id):
    """Display order confirmation page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    context = {
        'order': order,
        'show_payment_instructions': order.payment_status == 'pending'
    }
    return render(request, 'orders/order_confirmation.html', context)

def resend_confirmation_email(request, order_id):
    """Resend order confirmation email"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access this feature.')
        return redirect('accounts:login')
        
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    try:
        order.send_order_confirmation_email()
        messages.success(request, 'Confirmation email has been resent.')
    except Exception as e:
        messages.error(request, 'Failed to send confirmation email. Please try again later.')
    
    return redirect('orders:order_detail', order_id=order.order_id)