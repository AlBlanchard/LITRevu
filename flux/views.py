from itertools import chain
from django.shortcuts import render
from django.db.models import CharField, Value
from tickets.models import Ticket, Review


def flux(request):
    """Affiche le flux d'activités de l'utilisateur."""
    followed_users = request.user.following.values_list("followed_user", flat=True)

    # Récupérer les critiques visibles (de l'utilisateur + des utilisateurs suivis)
    reviews = Review.objects.filter(user__in=list(followed_users) + [request.user])
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    # Récupérer les tickets visibles (de l'utilisateur + des utilisateurs suivis)
    tickets = Ticket.objects.filter(user__in=list(followed_users) + [request.user])
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    # Trier tout en ordre antéchronologique (du plus récent au plus ancien)
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(
        request, "flux/flux.html", {"posts": posts, "is_personal_view": False}
    )


# Si une personne B fait un review sur ticket de A et qu'une personne C est abboné à B, la personne A verra t elle les reviews de B sur ses tickets ?
# Si la personne B suit la A mais pas l'inverse, la personne A verra t elle les reviews de B ?
# Filtre : porter sur tous les reviews sur les tickets qui m'appartiennent


def self_posts(request):
    """Affiche uniquement les posts de l'utilisateur"""
    user = request.user

    # Récupérer les tickets de l'utilisateur
    self_tickets = Ticket.objects.filter(user=user).annotate(
        content_type=Value("TICKET", CharField())
    )

    # Récupérer les critiques de l'utilisateur
    self_reviews = Review.objects.filter(user=user).annotate(
        content_type=Value("REVIEW", CharField())
    )

    # Récupérer les critiques laissées par d'autres utilisateurs sur mes tickets
    reviews_on_self_tickets = Review.objects.filter(ticket__user=user).exclude(
        user=user
    )
    reviews_on_self_tickets = reviews_on_self_tickets.annotate(
        content_type=Value("REVIEW_ON_SELF_TICKET", CharField())
    )

    # Trier toutes les entrées par date de création, du plus récent au plus ancien
    posts = sorted(
        chain(self_tickets, self_reviews, reviews_on_self_tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(
        request,
        "flux/flux.html",
        {
            "posts": posts,
            "is_personal_view": True,
        },
    )
