from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('user-verification/<str:token>/', views.UserVerificationView.as_view(), name='user_verification_token'),
    path('user-verification/', views.UserVerificationView.as_view(), name='user_verification'),
    path('user-profile/', views.UserProfileView.as_view(), name='user_profile'),
]
