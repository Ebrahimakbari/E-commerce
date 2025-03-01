from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('user-verification/<str:token>/', views.UserVerificationView.as_view(), name='user_verification_token'),
    path('user-verification/', views.UserVerificationView.as_view(), name='user_verification'),
]
