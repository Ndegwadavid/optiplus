# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('store-locator/', views.store_locator, name='store_locator'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('brands/', views.brands, name='brands'),
    path('offers/', views.offers, name='offers'),
    path('faq/', views.faq, name='faq'),
    path('shipping/', views.shipping, name='shipping'),
    path('returns/', views.returns, name='returns'),
    path('size-guide/', views.size_guide, name='size_guide'),
]