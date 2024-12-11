from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form class for users to create or edit booking
    """
    class Meta:
        model = Booking
        fields = ['occasion', 'occasion_type', 'notes']
