from django.contrib import admin

from tickets.models import Application, Ticket

class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Application, ApplicationAdmin)

class TicketAdmin(admin.ModelAdmin):

    date_heirarchy = "created_on"
    list_filter = ("status",)
    list_filter = ("ticket_type", "status", "priority", "application")
    list_display = (
        "id",
        "name",
        "active",
        "status",
        "priority",
        "application",
        "assigned_to",
        "submitted_by",
    )
    search_field = ["description"]


admin.site.register(Ticket, TicketAdmin)
