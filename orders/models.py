from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('is_paid', 'updated')

    def get_full_price(self):
        total = sum(item.get_price() for item in self.items.all())
        if self.discount:
            total = total - (self.discount/100) * total
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField()
    quantity = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'order items'
        verbose_name_plural = 'orders items'

    def get_price(self):
        return self.quantity * self.price


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(90)])

    def __str__(self):
        return self.code