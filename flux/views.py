from itertools import chain
from django.shortcuts import render
from django.db.models import CharField, Value, Q
from tickets.models import Ticket, Review


from django.db.models import Q


def flux(request):
    """Affiche le flux d'activités de l'utilisateur."""
    followed_users = request.user.following.values_list("followed_user", flat=True)

    # Reviews visibles : celles des suivis + soi-même + sur ses propres tickets
    reviews = Review.objects.filter(
        Q(user__in=list(followed_users) + [request.user]) | Q(ticket__user=request.user)
    ).annotate(content_type=Value("REVIEW", CharField()))

    # Tickets visibles : ceux des suivis + soi-même
    tickets = Ticket.objects.filter(
        user__in=list(followed_users) + [request.user]
    ).annotate(content_type=Value("TICKET", CharField()))

    # Fusion et tri antéchronologique
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

    # Trier toutes les entrées par date de création, du plus récent au plus ancien
    posts = sorted(
        chain(self_tickets, self_reviews),
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
