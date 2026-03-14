from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    LoginView,
    ForgotPasswordView,
    ForgotPasswordVerifyOtpView,
    ResetPasswordView,
    UserMeView,
    ChangePasswordView,
    ProfileUpdateView,
    ShippingAddressView


)

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/login/', LoginView.as_view(), name='login'),
    # refresh token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/forgot-password/verify-otp/', ForgotPasswordVerifyOtpView.as_view(), name='forgot-password-verify-otp'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('auth/user/me/', UserMeView.as_view(), name='user-profile'),
    path('auth/user/update-profile/', ProfileUpdateView.as_view(), name='update-profile'),

    path('user/shipping-address/', ShippingAddressView.as_view(), name='shipping-address'),

]
