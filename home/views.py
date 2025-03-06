from django.shortcuts import redirect, render
from django.views import View
from .models import Product, Category
from django.contrib import messages
from .tasks import get_bucket_list



class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, template_name='home/home.html', context={'products':products})


class ProductDetail(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs.get('slug'))
        if product.exists():
            return render(request, 'home/detail.html', {'product':product.first()})
        messages.error(request, message='product not found')
        return redirect('home:home')


class BucketListView(View):
    def get(self, request):
        objects = get_bucket_list()
        return render(request, 'home/bucket.html', {'objects':objects})