from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ["id", "title", "user", "time_created", "has_review"]
    list_filter = ["time_created"]
    search_fields = ["title", "user__username"]
    ordering = ["-time_created"]
    date_hierarchy = "time_created"


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ["id", "title", "user", "ticket", "time_created"]
    list_filter = ["time_created"]
    search_fields = ["user__username"]
    ordering = ["-time_created"]
    date_hierarchy = "time_created"
