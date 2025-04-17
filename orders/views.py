from django.shortcuts import redirect, render
from django.views import View




class CartView(View):
    def get(self, request):
        return render(request, 'orders/cart.html', context={})



class CartAddView(View):
    def post(self, request, product_id):
        return redirect('home:home')
