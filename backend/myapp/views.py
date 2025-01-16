from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Event, Ticket, Booking
from .serializers import EventSerializer, TicketSerializer, BookingSerializer,SignupSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create the user
            return Response({
                "status": "User created successfully",
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                "status": "Login successful",
                "username": data['user'].username,
                "access_token": data['access_token']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the current user's token
            refresh_token = request.auth  # The token sent in the Authorization header
             
            token = RefreshToken(refresh_token)
            # Blacklist the token (or just delete it if you're not using blacklisting)
            # Blacklist the refresh token
            token.blacklist()

            return Response({"status": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error logging out: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# Event list and detail views
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Booking views
class CreateBooking(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Get the event_id and ticket_count from the request body
        event_id = request.data.get('event')
        ticket_count = request.data.get('ticket_count')

        # Check if the event exists
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"status": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is authenticated (this is already enforced by the permission_classes)
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed("User must be authenticated")

        # Check if there are enough available tickets
        if event.available_tickets < ticket_count:
            return Response({"status": "Not enough available tickets"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the booking instance
        booking = Booking(user=user, event=event, ticket_count=ticket_count)

        # Save the booking
        booking.save()

        # Update the event's available tickets
        event.available_tickets -= ticket_count
        event.save()

        return Response({"status": "Booking successful", "booking_id": booking.id}, status=status.HTTP_201_CREATED)


class UpdateBooking(APIView):
    def put(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        ticket_count = request.data.get('ticket_count')

        if not ticket_count:
            return Response({"error": "Ticket count is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket_count = int(ticket_count)
        except ValueError:
            return Response({"error": "Invalid ticket count"}, status=status.HTTP_400_BAD_REQUEST)

        if ticket_count <= 0:
            return Response({"error": "Ticket count must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

        if booking.update_booking(ticket_count):
            serializer = BookingSerializer(booking)
            return Response({"status": "Booking updated successfully", "data": serializer.data})
        return Response({"error": "Unable to update booking. Insufficient available tickets."}, status=status.HTTP_400_BAD_REQUEST)


class CancelBooking(APIView):
    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)

        if booking.status == "Canceled":
            return Response({"error": "Booking has already been canceled."}, status=status.HTTP_400_BAD_REQUEST)

        if booking.cancel_booking():
            # serializer = BookingSerializer(booking)
            booking.delete() 
            return Response({"status": "Booking canceled successfully"} ,status=status.HTTP_200_OK )
        return Response({"error": "Unable to cancel booking"}, status=status.HTTP_400_BAD_REQUEST)

    

class UserBookings(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Retrieve all bookings for the authenticated user
        user = request.user
        bookings = Booking.objects.filter(user=user)
        
        # Serialize the bookings data
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)