from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from .models import *

# Custom User Creation Form with Role
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('management', 'Management'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

# Form for adding Popular Destinations
class PopularDestinationForm(ModelForm):
    class Meta:
        model = PopularDestination
        fields = '__all__'

class BookingForm(forms.ModelForm):
    departure_date = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(years=range(date.today().year, 2125)),
        initial=date.today,
        help_text="Please select a date from today onwards."
    )
    number_of_passengers = forms.IntegerField(min_value=1, initial=1, required=True)
    MODE_OF_TRAVEL_CHOICES = [
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('plane', 'Plane'),
    ]
    mode_of_travel = forms.ChoiceField(choices=MODE_OF_TRAVEL_CHOICES, required=True)

    class Meta:
        model = Booking
        fields = ['departure_date', 'number_of_passengers', 'mode_of_travel', 'from_location', 'to_location']

    def clean_departure_date(self):
        departure_date = self.cleaned_data.get('departure_date')
        if departure_date < date.today():
            raise forms.ValidationError("The departure date cannot be in the past.")
        return departure_date

class PassengerDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Name")
    address = forms.CharField(max_length=255, required=True, label="Address")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        required=True,
        label="Gender"
    )

# Payment Form with additional fields for transaction ID
class PaymentForm(forms.ModelForm):
    amount_paid = forms.DecimalField(max_digits=10, decimal_places=2, required=True,min_value=0, label="Amount Paid")  # Restore this field
    transaction_id = forms.CharField(max_length=50, required=True, label="Transaction ID")

    class Meta:
        model = Payment
        fields = ['payment_method', 'amount_paid', 'transaction_id']

    def save(self, commit=True):
        payment = super().save(commit=False)
        # Optionally add custom logic to process the payment
        if commit:
            payment.save()
        return payment

# Transport Selection Form
class TransportSelectionForm(forms.Form):
    transport = forms.ModelChoiceField(queryset=Transport.objects.all(), required=True)

# Seat Selection Form
class SeatSelectionForm(forms.Form):
    seat = forms.ModelChoiceField(queryset=Seat.objects.filter(is_booked=False), required=True)

    def clean_seat(self):
        seat = self.cleaned_data['seat']
        if seat.is_booked:
            raise forms.ValidationError('This seat is already booked. Please select another.')
        return seat
