import os
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="tickets_images/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # Permet d'ajouter l'attriubut objects pour le cleanup

    reviews: models.Manager[
        "Review"
    ]  # Correction de type pour le manager, sinon property ne fonctionne pas

    @property
    def has_review(self):
        """Vérifie si le ticket a une critique."""
        if self.reviews.all().exists():
            return True
        return False

    def delete(self, *args, **kwargs):
        """Supprime l'image associée avant de supprimer l'objet Ticket."""
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (créé par {self.user})"


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=120)
    body = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Critique de {self.ticket} par {self.user}"
