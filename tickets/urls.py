from django.urls import path
from .views import (
    create_ticket,
    update_ticket,
    delete_ticket,
    create_review,
    update_review,
    delete_review,
    create_ticket_and_review,
)

urlpatterns = [
    path("create/", create_ticket, name="ticket_create"),
    path("update/<int:ticket_id>/", update_ticket, name="ticket_update"),
    path("delete/<int:ticket_id>/", delete_ticket, name="ticket_delete"),
    path("reviews/create/<int:ticket_id>/", create_review, name="review_create"),
    path("reviews/update/<int:review_id>/", update_review, name="review_update"),
    path("reviews/delete/<int:review_id>/", delete_review, name="review_delete"),
    path("both/create/", create_ticket_and_review, name="ticket_and_review_create"),
]
