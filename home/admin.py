from django.contrib import admin
from .models import Category, Product
# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'price', 'created', 'updated']