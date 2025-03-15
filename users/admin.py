from django.contrib import admin
from .models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "time_created"]
    list_filter = ["time_created"]
    search_fields = ["title", "user__username"]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)
admin.site.register(UserFollows)
