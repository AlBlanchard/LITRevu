from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm
from .models import Ticket
from django.contrib import messages


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
        "tickets/ticket_form.html",
        {
            "form": form,
            "form_title": "Créer un ticket",
            "submit_text": "Envoyer",
        },
    )


def update_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket, id=ticket_id, user=request.user
    )  #  Check que l'utilisateur est bien le propriétaire du ticket

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket modifié avec succès !")
            return redirect("home")

    form = TicketForm(instance=ticket)
    return render(
        request,
        "tickets/ticket_form.html",
        {
            "form": form,
            "ticket": ticket,
            "form_title": "Modifier le ticket",
            "submit_text": "Mettre à jour",
        },
    )


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès !")
        return redirect("home")

    return render(request, "tickets/confirm_delete.html", {"ticket": ticket})
