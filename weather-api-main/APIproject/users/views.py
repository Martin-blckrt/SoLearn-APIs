from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer, LoginSerializer, ConfirmSerializer, CheckTokenSerializer
from django_email_verification import send_email, verify_token
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User




class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            send_email(serializer.save())
            return Response({'msg': 'Registration successful, verification email sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            success, user = verify_token(serializer.validated_data['token'])
            if success:
                user.is_active = True
                return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
            return Response('Invalid token', status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
      
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            except:
                return Response({'msg': 'Invalid Credentials or inactive account'}, status=status.HTTP_401_UNAUTHORIZED)
            if user is not None:
                login(request, user)
                auth_data = get_tokens_for_user(request.user)
                return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
            return Response({'msg': 'Invalid Credentials or inactive account'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

      
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) 
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'msg': 'Password successfully changed'}, status=status.HTTP_204_NO_CONTENT)


class TokenCheckView(APIView):

    def post(self, request):
        serializer = CheckTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                access_token_obj = AccessToken(serializer.validated_data['access_token'])
                user_id=access_token_obj['user_id']
                user=User.objects.get(id=user_id)
                return Response({'msg': f'Token is valid for user {user.email}', 'token_valid' : 1}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({'msg': 'Token is not valid', 'token_valid' : 0}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        