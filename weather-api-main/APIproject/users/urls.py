from django.urls import path, include
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, ConfirmationView, TokenCheckView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('confirmation', ConfirmationView.as_view(), name='confirmation'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('token-check/', TokenCheckView.as_view(), name='token_check'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]