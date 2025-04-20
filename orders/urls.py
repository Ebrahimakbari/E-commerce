from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/create-order/', views.OrderCreateView.as_view(), name='order_create'),
    path('cart/detail/<int:order_id>', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/detail/remove/<int:order_id>', views.OrderDetailRemoveView.as_view(), name='order_remove'),
    path('pay/<int:order_id>', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderPayVerifyView.as_view(), name='order_verify'),
    path('coupon/<int:order_id>', views.CouponApplyView.as_view(), name='coupon_apply'),
]