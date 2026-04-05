import logging
from datetime import datetime

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_otp_email_task(self, user_email, user_first_name, otp, subject):
    """
    Send OTP email asynchronously via Celery.
    """
    try:
        html_message = render_to_string(
            'email/otp_email.html',
            {'otp': otp, 'user': {'first_name': user_first_name}}
        )

        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        email.content_subtype = 'html'
        email.send()

        logger.info(
            f"OTP email sent successfully to {user_email} "
            f"(subject: {subject})"
        )

    except Exception as exc:
        logger.error(
            f"Failed to send OTP email to {user_email}: {exc}"
        )
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email_task(self, user_email, first_name, last_name):
    """
    Send a welcome/account confirmation email after successful OTP verification.
    """
    try:
        html_message = render_to_string(
            'email/welcome_email.html',
            {
                'first_name': first_name,
                'last_name': last_name,
                'email': user_email,
                'year': datetime.now().year,
            }
        )

        email = EmailMessage(
            subject='Welcome to Reactides — Your Account is Verified!',
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        email.content_subtype = 'html'
        email.send()

        logger.info(f"Welcome email sent successfully to {user_email}")

    except Exception as exc:
        logger.error(f"Failed to send welcome email to {user_email}: {exc}")
        raise self.retry(exc=exc)
