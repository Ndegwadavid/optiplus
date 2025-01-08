from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('brand/<slug:brand_slug>/', views.brand_products, name='brand_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('offers/', views.offers, name='offers'),
    path('brands/', views.brand_list, name='brand_list'),
]