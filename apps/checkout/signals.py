from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory


@receiver(post_save, sender=Order)
def create_order_status_history(sender, instance, created, **kwargs):

    if created:
        # First time order created → Save initial status
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status
        )
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