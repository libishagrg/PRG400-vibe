from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tour', 'tour_date', 'number_of_travelers', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'tour__title']
    ordering = ['-created_at']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
