from django.contrib import admin
from .models import Event, Ticket, Booking

# Customizing the Event Admin
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'location', 'total_tickets', 'available_tickets', 'price')
    search_fields = ('name', 'location')
    list_filter = ('date', 'location')

# Customizing the Ticket Admin
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'seat_number', 'price', 'status')
    search_fields = ('event__name', 'seat_number', 'status')
    list_filter = ('status', 'event__date')

# Customizing the Booking Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket_count', 'status', 'booking_date')
    search_fields = ('user__username', 'event__name')
    list_filter = ('status', 'event__date', 'user')

# Register the models with custom admin classes
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Booking, BookingAdmin)
