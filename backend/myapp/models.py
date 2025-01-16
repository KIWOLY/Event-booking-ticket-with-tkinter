from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def create_event(self):
        self.save()

    def update_event(self, name, date, time, location, price):
        self.name = name
        self.date = date
        self.time = time
        self.location = location
        self.price = price
        self.save()

    def delete_event(self):
        self.delete()

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Available")
    seat_number = models.IntegerField()

    def generate_ticket(self):
        self.save()

    def validate_ticket(self):
        return self.status == "Available"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_count = models.IntegerField()
    status = models.CharField(max_length=50, default="Reserved")
    booking_date = models.DateTimeField(auto_now_add=True)

    def create_booking(self, user, event, ticket_count):
        if event.available_tickets >= ticket_count:
            self.user = user
            self.event = event
            self.ticket_count = ticket_count
            event.available_tickets -= ticket_count
            event.save()
            self.save()
            return True
        return False

    def update_booking(self, ticket_count):
        if self.event.available_tickets >= ticket_count - self.ticket_count:
            self.event.available_tickets += self.ticket_count - ticket_count
            self.ticket_count = ticket_count
            self.event.save()
            self.save()
            return True
        return False

    def cancel_booking(self):
        self.event.available_tickets += self.ticket_count
        self.ticket_count = 0
        self.status = "Canceled"
        self.event.save()
        self.save()
        return True

