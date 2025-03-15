import os
from django.conf import settings
from django.core.management.base import BaseCommand
from tickets.models import Ticket


class Command(BaseCommand):
    help = "Supprime les fichiers images orphelins qui ne sont plus liés à un ticket."

    def handle(self, *args, **kwargs):
        image_folder = os.path.join(settings.MEDIA_ROOT, "tickets_images")
        existing_files = set(os.listdir(image_folder))

        used_files = set(
            ticket.image.name
            for ticket in Ticket.objects.all()
            if ticket.image and ticket.image.name
        )

        # Normalise les paths pour la comparaison
        orphaned_files = {
            file
            for file in existing_files
            if f"tickets_images/{file}" not in used_files
        }

        for file in orphaned_files:
            file_path = os.path.join(image_folder, file)
            os.remove(file_path)
            self.stdout.write(f"Fichier supprimé : {file}")

        self.stdout.write(
            getattr(self.style, "SUCCESS", lambda x: x)(
                "Nettoyage des images orphelines terminé !"
            )
        )
