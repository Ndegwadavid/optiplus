from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import EyewearProduct, Category, Brand
from django.db.models import Q 

def product_list(request):
    products = EyewearProduct.objects.filter(is_available=True)
    
    # Handle sorting
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    # Handle filters
    frame_shape = request.GET.get('frame_shape')
    frame_material = request.GET.get('frame_material')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if frame_shape:
        products = products.filter(frame_shape=frame_shape)
    if frame_material:
        products = products.filter(frame_material=frame_material)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'products/product_list.html', context)

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = EyewearProduct.objects.filter(
        category=category,
        is_available=True
    )
    
    # Handle sorting
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'category': category,
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'products/product_list.html', context)

def brand_products(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    products = EyewearProduct.objects.filter(
        brand=brand,
        is_available=True
    )
    
    # Handle sorting
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'brand': brand,
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(EyewearProduct, slug=slug, is_available=True)
    related_products = EyewearProduct.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = EyewearProduct.objects.filter(
            is_available=True
        ).filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(brand__name__icontains=query) |
            models.Q(category__name__icontains=query)
        ).distinct()
    else:
        products = EyewearProduct.objects.filter(is_available=True)

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'products/product_list.html', context)

def brand_list(request):
    brands = Brand.objects.filter(is_active=True)
    return render(request, 'products/brand_list.html', {'brands': brands})


def offers(request):
    """Display products that are currently on sale"""
    products = EyewearProduct.objects.filter(
        Q(sale_price__isnull=False) & 
        Q(is_available=True) & 
        Q(in_stock=True)
    ).order_by('-created_at')

    # Handle sorting
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('sale_price')
    elif sort == 'price_high':
        products = products.order_by('-sale_price')
    elif sort == 'discount':
        # Calculate highest discount percentage
        products = sorted(
            products,
            key=lambda x: ((x.price - x.sale_price) / x.price) * 100 if x.sale_price else 0,
            reverse=True
        )

    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'is_offers_page': True  # Flag to indicate we're on the offers page
    }
    
    return render(request, 'products/offers.html', context)

def search_products(request):
    query = request.GET.get('q', '')
    products = EyewearProduct.objects.filter(is_available=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    # Handle sorting
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    
    return render(request, 'products/product_list.html', context)