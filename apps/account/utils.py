from django.conf import settings
from django.core.mail import EmailMessage
from django.forms import ValidationError
from django.template.loader import render_to_string
from .models import (
    User,
    EmailOTP
)
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def send_registration_otp_email(user: User):
    # Get existing OTP object or create new one
    otp_obj, created = EmailOTP.objects.get_or_create(user=user)

    if not created and not otp_obj.can_resend():
        raise ValidationError("Please wait 1 minute before requesting a new OTP.")
    # Generate new OTP
    otp_code = otp_obj.generate_otp()   # assuming this sets self.otp
    otp_obj.save()

    html_message = render_to_string(
        'email/otp_email.html',
        {'otp': otp_obj.otp, 'user': user}
    )

    email = EmailMessage(
        subject='Your One-Time Password for Registration',
        body=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.content_subtype = 'html'
    return email.send()


def send_forgot_password_otp_email(user: User):
    otp_obj, created = EmailOTP.objects.get_or_create(user=user)
    
    if not created and not otp_obj.can_resend():
        raise ValidationError("Please wait 1 minute before requesting a new OTP.")
    # Generate new OTP
    otp_code = otp_obj.generate_otp()   # assuming this sets self.otp
    otp_obj.save()

    html_message = render_to_string(
        'email/otp_email.html',
        {'otp': otp_obj.otp, 'user': user}
    )

    email = EmailMessage(
        subject='You requested a password reset OTP',
        body=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.content_subtype = 'html'
    return email.send()

