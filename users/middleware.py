"""
Middleware

Permet de vérifier si l'utilisateur est connecté,
et de le rediriger vers la page de connexion si ce n'est pas le cas.
"""

from django.shortcuts import redirect
from django.conf import settings


def check_authentication(request):
    """Vérifie si l'utilisateur est connecté et redirige vers login si nécessaire."""
    allowed_paths = [settings.LOGIN_URL, "/users/register/", "/admin/"]

    if not request.user.is_authenticated and request.path not in allowed_paths:
        return redirect(settings.LOGIN_URL)

    return None


class LoginRequiredMiddleware:
    """Middleware Django qui force l'authentification."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = check_authentication(request)  # On délègue à la fonction
        return response if response else self.get_response(request)
