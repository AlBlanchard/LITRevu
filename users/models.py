from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models


class UserFollow(models.Model):
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
