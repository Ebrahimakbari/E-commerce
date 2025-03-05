from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', view=views.HomeView.as_view(), name='home'),
    path('products/<slug:slug>/', view=views.ProductDetail.as_view(), name='product_detail'),
]
