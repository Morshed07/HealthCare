from django.forms import ValidationError
from .models import (
    User,
    EmailOTP
)
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_otp_email_task


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def _send_otp_email(user: User, subject: str):
    """
    Generic function to send OTP emails with resend rate limiting.
    Gets or creates OTP, checks rate limit, generates OTP,
    and sends email asynchronously via Celery.
    """
    otp_obj, created = EmailOTP.objects.get_or_create(user=user)
    
    # If existing OTP and can't resend yet, raise error
    if not created and not otp_obj.can_resend():
        raise ValidationError("Please wait 1 minute before requesting a new OTP.")
    
    # Generate new OTP (this also saves it)
    otp_obj.generate_otp()
    
    # Send email asynchronously via Celery
    send_otp_email_task.delay(
        user_email=user.email,
        user_first_name=user.first_name,
        otp=otp_obj.otp,
        subject=subject
    )


def send_registration_otp_email(user: User):
    """Send OTP email for user registration"""
    return _send_otp_email(user, subject='Your One-Time Password for Registration')


def send_forgot_password_otp_email(user: User):
    """Send OTP email for password reset"""
    return _send_otp_email(user, subject='You requested a password reset OTP')
