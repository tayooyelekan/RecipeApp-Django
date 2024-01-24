from rest_framework.views import APIView
from rest_framework.response import Response 
from django.http import JsonResponse
from rest_framework import permissions, status
from .serializers import UserSerializer
from  .models import User
import jwt, datetime, bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import update_session_auth_hash

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    @extend_schema(
        request=OpenApiTypes.OBJECT, 
        examples=[
            OpenApiExample(
                "Registration",
                value={
                    "username": "john",
                    "email": "john@email.com",
                    "number": "090909090",
                    "password": "secret" 
                }
            )
        ],
        tags=["Users"]
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        email = request.data['email']
        username = request.data['username']
        number = request.data['number']
        password = request.data['password']

        # Check if email exists
        if User.objects.filter(email=email).exists():
            return Response('Email already exists')

        # Check if name exists    
        if User.objects.filter(username=username).exists():
            return Response('Username already exists')

        if User.objects.filter(number=number).exists():
            return Response('Phone Number already exists')    
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response({"message": "User Created Successfully", "data": UserSerializer(user).data, "status": status.HTTP_201_CREATED})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @extend_schema(
        request=OpenApiTypes.OBJECT, 
        examples=[
            OpenApiExample(
                "Login",
                value={
                    "email": "john@email.com",
                    "password": "secret" 
                }
            )
        ],
        tags=["Users"]
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        try:
            user = User.objects.get(email=email) 
        except User.DoesNotExist: 
            return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not user.check_password(password):
            return Response('Incorrect password!')
            
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
            
        return Response({
            'message': 'Login Successful',
            'user': serializer.data,
            'token': str(refresh.access_token)
        })
            
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @extend_schema(
        tags=["Users"]
    )
    def get(self, request):
        content = {
            'user': str(request.user),  # `request.user` is available from token
        }
        serializer = UserSerializer(request.user)
        return Response({ "data": serializer.data})


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @extend_schema(
        tags=["Users"]
    )
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class EditUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=OpenApiTypes.OBJECT, 
        examples=[
            OpenApiExample(
                "Edit User",
                value={
                    "number": "09109090919",
                }
            )
        ],
        tags=["Users"]
    )
    def put(self, request):
        user = request.user

        # Allow only one field edit at a time
        if "username" in request.data:
            if User.objects.filter(username=request.data["username"]).exists():
                return Response('Username already exists')
            user.username = request.data["username"]
        elif "email" in request.data:
            if User.objects.filter(email=request.data["email"]).exists():
                return Response('Email already exists') 
            user.email = request.data["email"]
        elif "number" in request.data:
            if User.objects.filter(number=request.data["number"]).exists():
                return Response('Phone Number already exists')
            user.number = request.data["number"]
        elif "fullName" in request.data: 
            user.fullName = request.data["fullName"]
        elif "bio" in request.data:
            user.bio = request.data["bio"] 
        elif "country" in request.data:
            user.country = request.data["country"]                            
            
        user.save()
        
        serializer = UserSerializer(user)
        return Response({ "data": serializer.data})

class DeleteUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)    
    
    @extend_schema(
        tags=["Users"]
    )
    def delete(self, request):
        user = request.user 
        user.delete()
        return Response('User deleted!')

class ListUsersView(APIView):
    permission_classes = [permissions.AllowAny,]

    @extend_schema(
        tags=["Users"]
    )
    def get(self, request):
        users = User.objects.all() 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)        

class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                "Change Password",
                value={
                    "old_password": "secret",
                    "new_password": "new_secret",
                },
            ),
        ],
        tags=["Users"],
    )
    def put(self, request):
        user = request.user
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        if not user.check_password(old_password):
            return Response('Incorrect password!')

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})   

