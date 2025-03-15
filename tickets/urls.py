from django.urls import path
from .views import create_ticket, update_ticket, delete_ticket

urlpatterns = [
    path("create/", create_ticket, name="ticket_create"),
    path("update/<int:ticket_id>/", update_ticket, name="ticket_update"),
    path("delete/<int:ticket_id>/", delete_ticket, name="ticket_delete"),
]
