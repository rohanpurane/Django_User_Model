from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('reset_password_link/', SendResetPasswordEmailView.as_view(), name='reset_password_link'),
    path('reset_password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

]


#  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),