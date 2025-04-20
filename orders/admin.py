from django.contrib import admin
from .models import Coupon, Order,OrderItem
# Register your models here.


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_paid', 'updated', 'created']
    inlines = [OrderItemInLine]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_active', 'valid_from', 'valid_to', 'discount']