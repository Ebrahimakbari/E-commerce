from django.urls import path
from . import views



app_name = 'api'
urlpatterns = [
    path('register/', views.UserRegisterViewAPI.as_view(), name='register_api'),
    path('users/user-activation/email/<str:token>/', views.UserAccountActivationAPI.as_view(), name='activation_email_api'),
    path('users/user-activation/sms/', views.UserAccountActivationAPI.as_view(), name='activation_sms_api'),
]
