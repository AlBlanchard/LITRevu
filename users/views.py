from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import LoginForm
from datetime import datetime


def global_variables(request):
    return {"timestamp": datetime.now().timestamp()}


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue")
            return redirect("home")

        # Stocker chaque erreur dans messages.error() pour qu’elles disparaissent après affichage
        for _, errors in form.errors.items():
            for error in errors:
                error_message = f"{error}"

                if "This password is too short" in error:
                    error_message = (
                        "Le mot de passe est trop court (minimum 8 caractères)."
                    )
                elif "This password is too common" in error:
                    error_message = "Ce mot de passe est trop courant, veuillez en choisir un plus sécurisé."
                elif "This password is entirely numeric" in error:
                    error_message = "Le mot de passe ne peut pas être uniquement composé de chiffres."
                elif "A user with that username already exists." in error:
                    error_message = "Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre."

                messages.error(request, f"{error_message}")

        return redirect("register")

    form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    form = LoginForm(request, data=request.POST)

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {username} !")
            return redirect("home")

        # return render(request, "users/login.html", {"error": "Invalid credentials"})
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        return redirect("login")

    form = LoginForm()
    return render(request, "users/login.html", {"form": form})
