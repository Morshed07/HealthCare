from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory
from celery import chain
from apps.checkout.tasks import (
    send_order_confirmation_email,
    send_admin_order_notification_email,
)


@receiver(post_save, sender=Order)
def create_order_status_history(sender, instance, created, **kwargs):

    if created:
        # First time order created → Save initial status
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status
        )

        # Send user confirmation email first, then admin notification
        chain(
            send_order_confirmation_email.s(instance.order_id),
            send_admin_order_notification_email.si(),
        ).apply_async()
    else:
        # Check if status changed
        last_status = (
            OrderStatusHistory.objects
            .filter(order=instance)
            .order_by("-updated_at")
            .first()
        )

        if last_status and last_status.status != instance.status:
            OrderStatusHistory.objects.create(
                order=instance,
                status=instance.status
            )