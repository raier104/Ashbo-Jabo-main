from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# Popular Destination Model
class PopularDestination(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destination_image = models.ImageField(upload_to='destinations/')
    destination_location = models.CharField(max_length=50)
    departure_location = models.CharField(max_length=50)
    travel_time_maximum = models.IntegerField()
    travel_time_minimum = models.IntegerField()

    def __str__(self):
        return f"{self.departure_location} - {self.destination_location}"

# Custom User model with approval for management users
class CustomUser(AbstractUser):
    is_management = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Add phone_number field

# Transport Model for bus, train, plane
class Transport(models.Model):
    TRANSPORT_TYPES = [
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('plane', 'Plane'),
    ]
    transport_type = models.CharField(choices=TRANSPORT_TYPES, max_length=10)
    company = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_location = models.CharField(max_length=50, default="Unknown")  # Add this field
    destination_location = models.CharField(max_length=50, default="Unknown")  # Add this field

    def __str__(self):
        return f"{self.company} ({self.transport_type})"

# Seat Model for tracking seat availability
class Seat(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.transport.company}"

    def book_seat(self):
        self.is_booked = True
        self.save()

# Booking Model to store booking details
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    passenger_address = models.CharField(max_length=255)
    passenger_gender = models.CharField(max_length=10)
    number_of_passengers = models.IntegerField(default=1)
    from_location = models.CharField(max_length=50, default="Unknown")  # Add default value
    to_location = models.CharField(max_length=50, default="Unknown")    # Add default value

    def __str__(self):
        return f"Booking for {self.passenger_name} on {self.transport.company}"

    def save_booking(self):
        # Update the seat to be booked
        self.seat.book_seat()
        self.save()

# Payment Model for handling payment status
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit/Debit Card'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=15)
    payment_status = models.BooleanField(default=False)  # True if successful
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)  # Track payment date

    def __str__(self):
        return f"Payment for {self.booking.passenger_name}"

# Model to handle management user approval requests
class ManagementUserRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for {self.user.username} - Approved: {self.is_approved}"
