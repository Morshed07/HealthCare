from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import (
    User,
    EmailOTP
)
from .utils import (
    send_registration_otp_email,
    send_forgot_password_otp_email,
    get_tokens_for_user
)
from apps.representative.models import Representative


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = (
            "id",
            "name",
            "email",
            "phone_number",
            "company",
            "designation",
            "representative_code",
            "is_active"
        )
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    representative = RepresentativeSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "representative",
            "is_verified"
        )
        read_only_fields = ("id", "is_verified")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "representative_code",
        )
        extra_kwargs = {
            "email": {"validators": []},
        }

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user:
            if user.is_verified:
                raise serializers.ValidationError(
                    "User with this email already exists.",
                    code="already_exists"
                )
            else:
                raise serializers.ValidationError(
                    "Account not verified.",
                    code="pending_verification"
                )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def validate_representative_code(self, value):
        if not Representative.objects.filter(representative_code=value, is_active=True).exists():
            raise serializers.ValidationError("Invalid representative code.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            representative_code=validated_data.get('representative_code'),
            is_verified=False,
        )
        send_registration_otp_email(user)
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        if user.is_verified:
            raise serializers.ValidationError("This account is already verified.")

        otp_obj = EmailOTP.objects.filter(user=user).first()
        if not otp_obj or otp_obj.otp != otp:
            raise serializers.ValidationError("Invalid OTP.")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired. Please request a new one.")

        # If we reach here, OTP is valid
        user.is_verified = True
        user.save()
        return attrs
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account has been deactivated.")

        if not user.is_verified:
            # We raise a specific error so the frontend can redirect to Screen 3 (OTP)
            raise serializers.ValidationError("PENDING_VERIFICATION")

        # Standard JWT token generation
        tokens = get_tokens_for_user(user)

        user = UserSerializer(user).data  # Serialize user data to return in response

        # Return the user and tokens so the View can use them
        return {
            'tokens': tokens,
            'user': user
        }
