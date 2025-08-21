from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from orders.models import PurchaseOrder
from core.middlewares import get_current_user


@receiver(post_save, sender=PurchaseOrder)
def save_order_signal(sender, instance, created,**kwargs):

    # user = get_current_user()
    if created:
        print(f"New order {instance.order_number} Created.")
    elif not created and instance.pk:
        print(f"Order Updated {instance.order_number}")



