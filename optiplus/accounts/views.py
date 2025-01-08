# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from cart.models import Cart
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)
                
                # Handle cart merging
                session_cart_id = request.session.get('cart_id')
                if session_cart_id:
                    try:
                        session_cart = Cart.objects.get(id=session_cart_id)
                        user_cart = Cart.objects.filter(user=user).first()
                        
                        if user_cart:
                            # Merge the carts
                            for item in session_cart.items.all():
                                item.cart = user_cart
                                item.save()
                            session_cart.delete()
                        else:
                            # Assign session cart to user
                            session_cart.user = user
                            session_cart.save()
                    except Cart.DoesNotExist:
                        pass
                
                messages.success(request, f'Welcome back, {user.email}!')
                
                # Redirect to the next URL if it exists
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'title': 'Login'
    })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the user in
            login(request, user)
            
            # Handle cart merging if exists
            session_cart_id = request.session.get('cart_id')
            if session_cart_id:
                try:
                    session_cart = Cart.objects.get(id=session_cart_id)
                    session_cart.user = user
                    session_cart.save()
                except Cart.DoesNotExist:
                    pass
                    
            messages.success(request, 'Your account has been created successfully!')
            return redirect('accounts:register_success')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'title': 'Register'
    })

def register_success(request):
    return render(request, 'accounts/register_success.html')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')