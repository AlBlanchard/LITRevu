from django.contrib import admin
from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "time_created", "has_review"]
    list_filter = ["time_created"]
    search_fields = ["title", "user__username"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "ticket", "time_created"]
    list_filter = ["time_created"]
    search_fields = ["user__username"]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
