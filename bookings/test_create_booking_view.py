from django.utils import timezone
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from community_centre.models import CommunityCentre
from .models import TimeSlot, Booking


class TestCreateBookingView(TestCase):
    def setUp(self):
        # Common setup for tests in this class

        # Create a CommunityCentre instance
        self.community_centre = CommunityCentre.objects.create(
            name='Evergreen Community Centre',
            description='A community space for all types of events.',
            address='123 Evergreen St.',
            operating_start_day=1,
            operating_end_day=5,
            opening_time='09:00:00',
            closing_time='17:00:00'
        )

        self.user = User.objects.create_user(
            username='testuser', password='password')

        # Create a time slot in the future
        future_time = timezone.now() + timedelta(days=1)  # 1 day in the future
        self.time_slot = TimeSlot.objects.create(
            date=future_time.date(),
            start_time=future_time.time(),
            end_time=(future_time + timedelta(hours=1)).time(),
            community_centre=self.community_centre
        )
        self.url = reverse('create-booking', args=[self.time_slot.id])

    def test_redirects_if_not_logged_in(self):
        """Ensure unauthenticated users are redirected to the
        login page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_login'), response.url)

    def test_displays_form_for_logged_in_user(self):
        """Ensure the booking form is displayed to authenticated users."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/create_booking.html')
