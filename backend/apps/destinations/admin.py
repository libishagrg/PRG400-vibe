from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'continent', 'is_featured', 'created_at']
    list_filter = ['continent', 'is_featured']
    search_fields = ['name', 'country']
    list_editable = ['is_featured']
    ordering = ['name']
