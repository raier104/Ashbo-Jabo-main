# admin.py in the Bookings app

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Transport, Seat, Booking, Payment, ManagementUserRequest, PopularDestination

admin.site.register(Transport)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(ManagementUserRequest)
admin.site.register(PopularDestination)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_management', 'is_approved', 'is_staff')
    list_filter = ('is_management', 'is_approved', 'is_staff')
    actions = ['approve_management_users']

    def approve_management_users(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} management user(s) approved successfully.')