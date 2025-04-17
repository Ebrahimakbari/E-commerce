from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from home.models import Product
from .forms import AddToCartForm
from .cart import Cart



class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', context={'cart':cart})



class CartAddView(View):
    def post(self, request, product_id):
        c_form = AddToCartForm(request.POST)
        product = Product.objects.filter(pk=product_id)
        if not product.exists():
            messages.error(request, 'invalid product!!')
            return redirect('home:home')
        if c_form.is_valid():
            cart = Cart(request)
            product = product.first()
            cart.add(product, c_form.cleaned_data['quantity'])
            cart.save()
            messages.success(request, f'product {product.name} added to cart')
            return redirect('orders:cart')
        messages.error(request, 'invalid product quantity!')
        return redirect('home:home')
