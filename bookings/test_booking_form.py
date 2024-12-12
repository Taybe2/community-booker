from django.test import TestCase
from .forms import BookingForm

# Create your tests here.


class TestBookingForm(TestCase):

    def test_occasion_is_required(self):
        """Test for the 'occasion' field"""
        form = BookingForm({
            'occasion': '',
            'occasion_type': 'private',
            'notes': 'Hello!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="Occasion was not provided, but the form is valid"
        )

    def test_occasion_type_is_required(self):
        """Test for the 'occasion_type' field"""
        form = BookingForm({
            'occasion': 'some',
            'occasion_type': '',
            'notes': 'Hello!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="Occasion type was not provided, but the form is valid"
        )

    def test_notes_are_optional(self):
        """Test that the 'notes' field is optional"""
        form = BookingForm({
            'occasion': 'Birthday Party',
            'occasion_type': 'private',
        })
        self.assertTrue(
            form.is_valid(),
            msg="Notes are optional, but the form is invalid without them"
        )

    def test_invalid_occasion_type(self):
        """Test for invalid value in the 'occasion_type' field"""
        form = BookingForm({
            'occasion': 'Birthday Party',
            'occasion_type': 'invalid_choice',
            'notes': 'Celebrating!'
        })
        self.assertFalse(
            form.is_valid(),
            msg="An invalid occasion type was provided, but the form is valid"
        )
        self.assertIn(
            'occasion_type',
            form.errors,
            msg="Occasion type field did not raise an error for invalid input")
