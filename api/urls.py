from django.urls import path
from . import views



app_name = 'api'
urlpatterns = [
    path('register/', views.UserRegisterViewAPI.as_view(), name='register_api'),
]
