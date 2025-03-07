from django.shortcuts import redirect, render
from django.views import View
from .models import Product, Category
from django.contrib import messages
from . import tasks



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
        objects = tasks.get_bucket_list()
        return render(request, 'home/bucket.html', {'objects':objects})


class DeleteObjectBucketView(View):
    def get(self, request, key):
        tasks.delete_obj_bucket.delay(key)
        messages.success(request, 'object will delete soon...')
        return redirect('home:bucket')


class DownloadObjectBucketView(View):
    def get(self, request, key):
        tasks.download_obj_bucket.delay(key)
        messages.success(request, 'object will download soon...')
        return redirect('home:bucket')