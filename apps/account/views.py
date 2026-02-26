from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    UserSerializer,

)
from .utils import (
    send_registration_otp_email
)
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            errors = serializer.errors

            if 'email' in errors:
                error = serializer.errors['email'][0]

                if hasattr(error, 'code') and error.code == "pending_verification":
                    email = request.data.get('email')
                    user = User.objects.get(email=email)

                    send_registration_otp_email(user)

                    return Response({
                        "message": "Account already exists but is not verified. A new OTP has been sent.",
                        "action": "REDIRECT_TO_VERIFY",
                        "email": email
                    }, status=status.HTTP_200_OK)

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Normal registration flow
        serializer.save()
        return Response({
            "message": "Registration successful. Please verify your email.",
            "email": request.data.get('email')
        }, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                "message": "Account verified successfully. You can now log in."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        # Handle custom validation errors (like PENDING_VERIFICATION)
        errors = serializer.errors
        if "PENDING_VERIFICATION" in str(errors):
            return Response({
                "message": "Please verify your account.",
                "action": "REDIRECT_TO_VERIFY",
                "email": request.data.get('email')
            }, status=status.HTTP_403_FORBIDDEN)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)