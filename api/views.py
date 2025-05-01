from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterUserSerializer
from rest_framework.response import Response



class UserRegisterViewAPI(APIView):
    serializer_class = RegisterUserSerializer
    
    def post(self, request):
        srz_data = self.serializer_class(data=request.data, context={'request':request})
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)