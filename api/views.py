from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets

from home.models import Category, Product
from orders.models import Order
from .serializers import (
    CategorySerializer,
    OrderSerializer,
    ProductSerializer,
    RegisterUserSerializer,
    EmailOtpSerializer,
    SmsOtpSerializer,
    LoginUserSerializer,
    LogoutUserSerializer,
    ResetPasswordSerializer,
    )
from rest_framework.response import Response
from utils import IsAdminUserOrReadOnly, IsOwnerOrAdmin


class UserRegisterViewAPI(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        srz_data = self.serializer_class(
            data=request.data, context={'request': request})
        if srz_data.is_valid():
            srz_data.save()
            return Response(
                data={
                    'data': srz_data.data,
                    'message': 'your account has been created please activate your account with chosen method!'
                    },
                    status=status.HTTP_201_CREATED
                    )
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountActivationAPI(APIView):
    def post(self, request, token=None):
        srz_data = SmsOtpSerializer(data=request.data)
        if srz_data.is_valid():
            return Response(data={
                'message': f'user with {srz_data.validated_data['phone_number']} phone_number is activated!!'
            }, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, token=None):
        if token:
            srz_data = EmailOtpSerializer(data={'token': token})
            if srz_data.is_valid():
                return Response(data={
                    'message': f'user with {srz_data.validated_data['email']} email is activated!!'
                }, status=status.HTTP_200_OK)
            return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data={'message': 'use post for sms verification!'},
            status=status.HTTP_400_BAD_REQUEST
            )


class LoginUserAPI(APIView):
    def post(self, request):
        srz_data = LoginUserSerializer(data=request.data)
        if srz_data.is_valid():
            tokens = srz_data.validated_data['tokens']
            user_info = srz_data.validated_data['user-info']
            return Response(data={'tokens': tokens, 'user-info': user_info}, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        srz_data = LogoutUserSerializer(data=request.data)
        if srz_data.is_valid():
            return Response(
                data={'message': 'you logged out successfully!!'},
                status=status.HTTP_200_OK
                )
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request:HttpRequest):
        srz_data = ResetPasswordSerializer(data=request.data, context={'request':request})
        srz_data.is_valid(raise_exception=True)
        return Response(
            data={'message':f'password for user {request.user.phone_number} is changed!'},
            status=status.HTTP_200_OK
            )


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly,]
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.default_objects.all()
        return Product.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly,]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class OrderViewAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()