# core/views.py
from django.shortcuts import render
from products.models import EyewearProduct, Brand, Category

def home(request):
    # Get featured products
    featured_products = EyewearProduct.objects.filter(
        is_available=True,
        featured=True
    )[:8]  # Limit to 8 featured products
    
    # Get popular brands
    popular_brands = Brand.objects.filter(is_active=True)[:6]
    
    # Get all active categories
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'featured_products': featured_products,
        'popular_brands': popular_brands,
        'categories': categories
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission here
        pass
    return render(request, 'core/contact.html')

def store_locator(request):
    # You can add store locations data here
    stores = [
        {
            'name': 'Moi Avenue Branch',
            'address': 'Opposite Imenti House – Nacico Chambers',
            'city': 'Nairobi',
            'phone': '+254 702 220 545',
            'hours': 'Monday – Friday: 9:00am – 6:00pm\nSaturday: 9:00am – 4:00pm'
        },
        {
            'name': 'Ronald Ngala Branch',
            'address': 'Opposite The Post Office',
            'city': 'Nairobi',
            'phone': '+254 105 165 560',
            'hours': 'Monday – Friday: 9:00am – 6:00pm\nSaturday: 9:00am – 4:00pm'
        }
    ]
    return render(request, 'core/store_locator.html', {'stores': stores})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def store_locator(request):
    return render(request, 'core/store_locator.html')

def book_appointment(request):
    return render(request, 'core/book_appointment.html')

def brands(request):
    brands = Brand.objects.all()
    return render(request, 'core/brands.html', {'brands': brands})

def offers(request):
    offers = EyewearProduct.objects.filter(sale_price__isnull=False)
    return render(request, 'core/offers.html', {'offers': offers})

def faq(request):
    return render(request, 'core/faq.html')

def shipping(request):
    return render(request, 'core/shipping.html')

def returns(request):
    return render(request, 'core/returns.html')

def size_guide(request):
    return render(request, 'core/size_guide.html')