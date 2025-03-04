from django.shortcuts import render
from django.views import View
from .models import Product, Category



class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, template_name='home/home.html', context={'products':products})