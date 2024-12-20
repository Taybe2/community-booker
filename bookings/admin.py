from django.contrib import admin
from .models import Booking, TimeSlot

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters and read-only fields.
    """
    list_display = ('user', 'community_centre', 'time_slot', 'created_at')
    list_filter = ('community_centre', 'time_slot__date')
    search_fields = ('user__username', 'community_centre__name')
    readonly_fields = ('slug',)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, field filters and
    fields for search
    """
    list_display = (
        'community_centre',
        'date',
        'start_time',
        'end_time',
        'created_at')
    list_filter = ('community_centre', 'date')
    search_fields = ('community_centre__name', 'date')
