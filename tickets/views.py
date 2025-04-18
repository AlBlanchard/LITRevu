from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from django.contrib import messages
from django.core.exceptions import ValidationError


def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)  # Prend en charge les fichiers

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Associe l'utilisateur connecté
            messages.success(request, "Ticket créé avec succès !")
            ticket.save()
            return redirect("home")

    form = TicketForm()
    return render(
        request,
        "tickets/form.html",
        {
            "ticket_form": form,
            "form_title": "Créer un ticket",
            "submit_text": "Envoyer",
            "include_ticket_form": True,
        },
    )


def update_ticket(request, ticket_id):
    #  Check que l'utilisateur est bien le propriétaire du ticket
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket modifié avec succès !")
            return redirect("self_posts")

    form = TicketForm(instance=ticket)
    return render(
        request,
        "tickets/form.html",
        {
            "ticket_form": form,
            "ticket": ticket,
            "include_ticket_form": True,
            "form_title": "Modifier votre ticket",
            "submit_text": "Mettre à jour",
        },
    )


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès !")
        return redirect("self_posts")

    return render(
        request,
        "tickets/confirm_delete.html",
        {"ticket": ticket, "is_ticket": True},
    )


# ---- REVIEW -----


def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user

            try:
                review.full_clean()
                review.save()
                messages.success(request, "Critique postée avec succès !")
                return redirect("home")

            except ValidationError as e:
                messages.error(request, e.messages[0])
                return redirect("home")

    form = ReviewForm()

    return render(
        request,
        "tickets/form.html",
        {
            "review_form": form,
            "ticket": ticket,
            "form_title": "Créer une critique",
            "submit_text": "Envoyer",
            "include_ticket": True,
            "include_review_form": True,
            "rating_range": ["5", "4", "3", "2", "1"],
        },
    )


def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    current_rating = str(review.rating)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Avis modifié avec succès !")
            return redirect("self_posts")

    form = ReviewForm(instance=review)
    return render(
        request,
        "tickets/form.html",
        {
            "review_form": form,
            "review": review,
            "include_ticket": True,
            "include_review_form": True,
            "update": True,
            "form_title": "Modifier votre critique",
            "submit_text": "Mettre à jour",
            "current_rating": current_rating,
            "rating_range": ["5", "4", "3", "2", "1"],
        },
    )


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "L'avis a été supprimé avec succès !")
        return redirect("self_posts")

    return render(request, "tickets/confirm_delete.html", {"review": review})


# ---- Critique -----
def create_ticket_and_review(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, prefix="ticket")
        review_form = ReviewForm(request.POST, prefix="review")

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            messages.success(request, "Ticket et avis créés avec succès !")
            return redirect("home")

    # Evite les conflits avec les champs du même nom
    ticket_form = TicketForm(prefix="ticket")
    review_form = ReviewForm(prefix="review")

    return render(
        request,
        "tickets/form.html",
        {
            "ticket_form": ticket_form,
            "review_form": review_form,
            "form_title": "Créer un ticket et une critique",
            "submit_text": "Envoyer",
            "include_ticket_form": True,
            "include_review_form": True,
            "rating_range": ["5", "4", "3", "2", "1"],
        },
    )
