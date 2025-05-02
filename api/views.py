from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import (
    RegisterUserSerializer,
    EmailOtpSerializer,
    SmsOtpSerializer,
    LoginUserSerializer,
    LogoutUserSerializer
    )
from rest_framework.response import Response


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
        return Response(data={'message': 'use post for sms verification!'}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(data={'message': 'you logged out successfully!!'}, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
