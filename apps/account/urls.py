from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    LoginView


)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/login/', LoginView.as_view(), name='login'),

]
