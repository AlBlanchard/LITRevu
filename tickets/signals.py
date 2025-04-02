from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Ticket
import os
from django.conf import settings


@receiver(post_delete, sender=Ticket)
def delete_ticket_image(sender, instance, **kwargs):
    """Supprime l'image du ticket lors de la suppression."""
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
        if os.path.isfile(image_path):
            os.remove(image_path)
