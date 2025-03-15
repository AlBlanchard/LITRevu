from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="tickets_images/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    has_review = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (créé par {self.user})"


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=120)
    body = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Critique de {self.ticket} par {self.user}"


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        unique_together = ("user", "followed_user")

    def clean(self):
        if self.user == self.followed_user:
            raise ValidationError("Vous ne pouvez pas vous suivre vous-même.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} suit {self.followed_user}"
