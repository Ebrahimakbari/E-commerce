from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from home.models import Product
from orders.models import Order, OrderItem
from .forms import AddToCartForm
from .cart import Cart
from django.conf import settings
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', context={'cart': cart})


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
        items = [OrderItem(order=order, product=Product.objects.get(pk=int(item['pk'])), price=int(
            item['price']), quantity=item['quantity']) for item in user_session.values()]
        OrderItem.objects.bulk_create(items)
        del request.session['cart']
        messages.success(request, 'added to db!')
        return redirect(reverse('orders:order_detail', kwargs={'order_id': order.id}))


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.filter(pk=order_id)
        if order.exists():
            return render(request, 'orders/cart_detail.html', {'order': order.first()})
        messages.error(request, 'invalid order id !!')
        return redirect('orders:cart')


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            request.session['order_id'] = order_id
        except Order.DoesNotExist:
            return JsonResponse({'status': False, 'code': 'order not found'}, status=404)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_full_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                    'content-length': str(len(data))}

        try:
            response = requests.post(
                ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return JsonResponse(
                        {
                            'status': True,
                            'url': ZP_API_STARTPAY + str(response_data['Authority']),
                            'authority': response_data['Authority']
                            }
                        )
                else:
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])}, status=400)
            return JsonResponse({'status': False, 'code': 'invalid response'}, status=400)

        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'}, status=504)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'}, status=502)


class OrderPayVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        authority = request.GET.get('authority')
        order_id = int(request.session.get('order_id', 0))
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'status': False, 'code': 'order not found'}, status=404)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_full_price(),
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                    'content-length': str(len(data))}

        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                order.is_paid = True
                order.save()
                return JsonResponse({'status': True, 'RefID': response_data['RefID']})
            else:
                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        return JsonResponse(
            {'status': False, 'code': 'invalid response', 'response': response.json()}, status=400
            )
