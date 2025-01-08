from django.utils import timezone
import uuid
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]

    PAYMENT_METHOD = [
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        # Comment these out for future implementation
        # ('card', 'Credit/Debit Card'),
        # ('paypal', 'PayPal'),
    ]

    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='mpesa')
    mpesa_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_notes = models.TextField(blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            timestamp = timezone.now().strftime('%y%m%d%H%M%S')  # Use Django's timezone
            unique_id = str(uuid.uuid4().hex)[:6]
            self.order_id = f'OPT{timestamp}{unique_id}'
        super().save(*args, **kwargs)

    def generate_order_id(self):
        while True:
            now = timezone.now()
            year = str(now.year)[-2:]
            month = str(now.month).zfill(2)
            random_str = str(uuid.uuid4().int)[:6]
            order_id = f'OPT{year}{month}{random_str}'
        
        # Check if this order_id already exists
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id


    def send_order_confirmation_email(self):
        """Send order confirmation email"""
        subject = f'Order Confirmation - {self.order_id}'
        html_message = render_to_string('orders/emails/order_confirmation.html', {
            'order': self,
            'items': self.items.all()
        })
        
        # For development, use console email backend
        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            html_message=html_message,
            fail_silently=False,
        )
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.EyewearProduct', on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # Store name in case product is deleted
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order {self.order.order_id}"