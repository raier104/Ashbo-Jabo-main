from django.contrib import admin
from django.urls import path
from Bookings import views  # Import views from the 'Bookings' app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('about_us/', views.about_us, name="about_us"),
    path('book/', views.book, name="book"),  # Booking page view
    path('popular_destination/', views.popular_destination, name="popular_destination"),
    path('add_popular_destination/', views.add_popular_destination, name="add_popular_destination"),
    path('delete_popular_destination/<str:id>/', views.delete_popular_destination, name="delete_popular_destination"),
    path('update_popular_destination/<str:id>/', views.update_popular_destination, name="update_popular_destination"),
    path('log_in/', views.log_in, name="log_in"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('logout/', views.custom_logout, name='logout'),
    path('book_transport/', views.book_transport, name='book_transport'),
    path('seat_selection/<int:transport_id>/', views.seat_selection, name='seat_selection'),
    path('passenger_details/<int:seat_id>/', views.passenger_details, name='passenger_details'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment_success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('print_receipt/<int:booking_id>/', views.print_receipt, name='print_receipt'),
]
