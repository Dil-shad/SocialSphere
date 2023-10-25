from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserModelSerializer,UserLoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

# Create your views here.


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()

            # Generate a token for the registered user
            token, created = Token.objects.get_or_create(user=user)

            return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # username = request.data.get('username')
        # password = request.data.get('password')
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
        
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                # If authentication is successful, create or retrieve a token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
