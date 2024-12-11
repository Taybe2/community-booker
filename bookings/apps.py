from django.apps import AppConfig


class BookingsConfig(AppConfig):
    """
    Provides primary key type for bookings app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'
