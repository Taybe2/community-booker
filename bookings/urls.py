from django.urls import path
from . import views

urlpatterns = [
    path('time-slots/', views.time_slot_view, name='time_slots'),
    path(
        'time-slots/<slug:booking_slug>/',
        views.time_slot_view,
        name='time_slots'),
    path(
        'booking/<int:time_slot_id>/',
        views.create_booking_view,
        name='create-booking'),
    path('my-bookings/', views.my_bookings_view, name='my-bookings'),
    path(
        'booking/<slug:slug>/cancel/',
        views.cancel_booking,
        name='cancel-booking'),
    path(
        'booking/<slug:slug>/edit/',
        views.edit_booking_view,
        name='edit-booking'),
    path(
        'booking/<slug:slug>/edit/<int:slot_id>/',
        views.edit_booking_view,
        name='edit-booking'),
    path(
        'booking/<slug:booking_slug>/change-time-slot/',
        views.change_time_slot_view,
        name='change-time-slot'),
]
