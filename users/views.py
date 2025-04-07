from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm, FollowUserForm
from .models import UserFollow
from django.views.decorators.cache import never_cache

User = get_user_model()


def global_variables(request):
    return {"timestamp": datetime.now().timestamp()}


@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

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
                    error_message = (
                        "Mot de passe est trop courant, choisissez en un plus sécurisé."
                    )
                elif "This password is entirely numeric" in error:
                    error_message = (
                        "Le mot de passe ne peut pas contenir uniquement des chiffres."
                    )
                elif "A user with that username already exists." in error:
                    error_message = (
                        "Nom d'utilisateur déjà pris. Veuillez en choisir un autre."
                    )

                messages.error(request, f"{error_message}")

        return redirect("register")

    form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request, data=request.POST)

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {username} !")
            return redirect("home")

        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        return redirect("login")

    form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def subscribe(request):
    form = FollowUserForm()
    followed_users = request.user.following.all()
    followers = request.user.followers.all()

    if request.method == "POST":
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            followed_user = get_object_or_404(User, username=username)

            if followed_user == request.user:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même !")
            elif UserFollow.objects.filter(
                user=request.user, followed_user=followed_user
            ).exists():
                messages.error(request, "Vous suivez déjà cet utilisateur.")
            else:
                UserFollow.objects.create(
                    user=request.user, followed_user=followed_user
                )
                messages.success(
                    request, f"Vous suivez maintenant {followed_user.username}."
                )

            return redirect("subscriptions")

        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(request, error)
        return redirect("subscriptions")

    return render(
        request,
        "users/subscriptions.html",
        {
            "form": form,
            "followed_users": followed_users,
            "followers": followers,
        },
    )


def unfollow_user(request, followed_user_id):
    followed_user = get_object_or_404(User, id=followed_user_id)
    subscription = UserFollow.objects.filter(
        user=request.user, followed_user=followed_user
    )

    if subscription.exists():
        subscription.delete()
        messages.success(request, f"Vous ne suivez plus {followed_user.username}.")
    else:
        messages.error(request, "Vous ne suivez pas cet utilisateur.")

    return redirect("subscriptions")


def list_of_follow(request):
    followed_users = request.user.following.all()
    followers = request.user.followers.all()

    return render(
        request,
        "users/subscriptions.html",
        {"followed_users": followed_users, "followers": followers},
    )
