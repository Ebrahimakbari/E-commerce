from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from home.models import Product
from orders.models import Order, OrderItem
from .forms import AddToCartForm
from .cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin



class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', context={'cart':cart})


class CartAddView(LoginRequiredMixin, View):
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


class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        cart = Cart(request)
        if cart.remove(product_id):
            cart.save()
            messages.success(request, 'item deleted!')
            return redirect('orders:cart')
        messages.error(request, 'no product in cart!')
        return redirect('home:home')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_session = request.session.get('cart')
        if not user_session:
            messages.error(request, 'orders is empty!!')
            return redirect('orders:cart')
        order, created = Order.objects.update_or_create(user=user)
        items = [OrderItem(order=order, product=Product.objects.get(pk=int(item['pk'])), price=int(item['price']), quantity=item['quantity']) for item in user_session.values()]
        OrderItem.objects.bulk_create(items)
        del request.session['cart']
        messages.success(request, 'added to db!')
        return redirect(reverse('orders:order_detail', kwargs={'order_id':order.id}))


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.filter(pk=order_id)
        if order.exists():
            return render(request, 'orders/cart_detail.html', {'order':order.first()})
        messages.error(request, 'invalid order id !!')
        return redirect('orders:cart')