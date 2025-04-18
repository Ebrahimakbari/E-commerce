from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from home.models import Product

User = get_user_model()



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('is_paid', 'updated')
    
    def get_full_price(self):
        return sum(item.get_price() for item in self.items.all())
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField()
    quantity = models.SmallIntegerField(default=1)
    
    class Meta:
        verbose_name = 'order items'
        verbose_name_plural = 'orders items'
    
    def get_price(self):
        return self.quantity * self.price