from django.urls import path
from . import views

urlpatterns = [
    path('time-slots/', views.time_slot_view, name='time_slots'),
    path('booking/<int:time_slot_id>/', views.create_booking_view, name='booking-details'),
]