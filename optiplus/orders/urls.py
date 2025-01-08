# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm/', views.order_confirmation, name='order_confirmation'),
    path('mpesa-payment/<str:order_id>/', views.mpesa_payment, name='mpesa_payment'),
    path('confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('resend-email/<str:order_id>/', views.resend_confirmation_email, name='resend_confirmation_email'),
]