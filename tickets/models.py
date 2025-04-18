import os
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Ticket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="tickets_images/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

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
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Empêche la création si le ticket a déjà une review."""
        # Vérifie d'abord que self.ticket existe bien
        if not self.ticket_id:
            return

        # pk est l'id de l'instance actuelle que créer temporairement Django
        # Permet la modification du ticket sans lever d'erreur
        # self.pk est None lors de la création d'une nouvelle instance
        # self.pk est définie lors de la modification d'une instance existante
        if self.ticket.reviews.exists() and not self.pk:
            raise ValidationError("Ce ticket a déjà une critique.")

    def __str__(self):
        return f"Critique de {self.ticket} par {self.user}"
