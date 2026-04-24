from django.contrib import admin
from .models import Tour, TourDate


class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'category', 'price_per_person', 'rating', 'is_featured', 'is_active']
    list_filter = ['category', 'difficulty', 'is_featured', 'is_active']
    search_fields = ['title', 'destination__name']
    list_editable = ['is_featured', 'is_active']
    inlines = [TourDateInline]
    ordering = ['-created_at']


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ['tour', 'start_date', 'end_date', 'available_spots', 'is_active']
    list_filter = ['is_active']
    ordering = ['start_date']
