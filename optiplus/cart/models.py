# cart/models.py
from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from products.models import EyewearProduct

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Cart {self.id} - {'User: ' + self.user.email if self.user else 'Session: ' + str(self.session_id)}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(EyewearProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return self.quantity * (self.product.sale_price or self.product.price)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    
    
def get_items_count(self):
        return sum(item.quantity for item in self.items.all())

def get_total(self):
        return sum(
            item.quantity * (item.product.sale_price or item.product.price) 
            for item in self.items.all()
        )