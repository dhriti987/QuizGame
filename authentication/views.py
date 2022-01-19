from urllib import response
from django.shortcuts import render
from rest_framework import generics,status

from authentication.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self,request):
        serializer_obj = self.serializer_class(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        user_data = serializer_obj.data

        user  = User.objects.get(email = user_data['email'])
        Token.objects.create(user = user)
         
        return Response(user_data,status=status.HTTP_201_CREATED)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response =  super(CustomObtainAuthToken,self).post(request, *args, **kwargs)
        token = Token.objects.get(key= response.data['token'])
        print(token)
        user = User.objects.get(id=token.user_id)
        return Response({
            'token':token.key,
            'user':RegisterSerializer(user).data
        })