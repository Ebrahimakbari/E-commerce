from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



app_name = 'api'
urlpatterns = [
    path('register/', views.UserRegisterViewAPI.as_view(), name='register_api'),
    path('users/user-activation/email/<str:token>/', views.UserAccountActivationAPI.as_view(), name='activation_email_api'),
    path('users/user-activation/sms/', views.UserAccountActivationAPI.as_view(), name='activation_sms_api'),
    path('users/login/', views.LoginUserAPI.as_view(), name='login_api'),
    path('users/logout/', views.LogoutUserAPI.as_view(), name='logout_api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/reset-password/', views.ResetPasswordAPI.as_view(), name='reset_password_api'),

]
