from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ChangePasswordSerializer,
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    UserSerializer,
    ForgotPasswordRequestSerializer,
    ForgotPasswordVerifyOtpSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    ProfileUpdateSerializer

)
from .utils import (
    send_registration_otp_email
)
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import update_last_login

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
            email = request.data.get('email')
            user = User.objects.get(email=email)
            update_last_login(None, user)
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


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save() 
        # -----------------------------

        return Response({
            "success": True,
            "message": "OTP sent"
        }, status=status.HTTP_200_OK)


class ForgotPasswordVerifyOtpView(APIView):
    def post(self, request):
        serializer = ForgotPasswordVerifyOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "OTP verified successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)
    

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            "success": True,
            "message": "Password reset successfully"
        }, status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            "success": True,
            "message": "Password changed successfully"
        }, status=status.HTTP_200_OK)
    

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({
            "success": True,
            "message": "User profile fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": True,
            "message": "Profile updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "success": True,
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
