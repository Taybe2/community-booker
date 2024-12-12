from django.utils import timezone
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from community_centre.models import CommunityCentre
from .models import TimeSlot, Booking


class TestCancelBookingView(TestCase):
    def setUp(self):
        # Common setup for tests in this class
        self.community_centre = CommunityCentre.objects.create(
            name='Evergreen Community Centre',
            description='A community space for all types of events.',
            address='123 Evergreen St.',
            operating_start_day=1,
            operating_end_day=5,
            opening_time='09:00:00',
            closing_time='17:00:00'
        )

        self.user1 = User.objects.create_user(
            username='testuser1',
            password='password1')
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='password2')

        # Create a time slot in the past
        past_time = timezone.now() - timedelta(days=1)  # 1 day in the past
        self.time_slot = TimeSlot.objects.create(
            date=past_time.date(),
            start_time=past_time.time(),
            end_time=(past_time + timedelta(hours=1)).time(),
            community_centre=self.community_centre
        )

        # Create a booking for user1 in the past time slot
        self.booking = Booking.objects.create(
            user=self.user1,
            time_slot=self.time_slot,
            community_centre=self.community_centre,
            slug='test-past-booking-slug'  # Manually setting a slug
        )

        # Create a time slot in the future
        future_time = timezone.now() + timedelta(days=1)  # 1 day in the future
        self.time_slot_future = TimeSlot.objects.create(
            date=future_time.date(),
            start_time=future_time.time(),
            end_time=(future_time + timedelta(hours=1)).time(),
            community_centre=self.community_centre
        )

        # Create a booking for user1 in the future time slot
        self.booking_future = Booking.objects.create(
            user=self.user1,
            time_slot=self.time_slot_future,
            community_centre=self.community_centre,
            slug='test-future-booking-slug'  # Manually setting a slug
        )

        # The URL for canceling the booking
        self.url_user1_past = reverse(
            'cancel-booking',
            args=[self.booking.slug]
            )
        self.url_user1_future = reverse(
            'cancel-booking',
            args=[self.booking_future.slug]
            )

    def test_redirects_if_not_logged_in(self):
        """Ensure unauthenticated users cannot access
        the cancel booking page."""
        response = self.client.get(self.url_user1_future)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_login'), response.url)

    def test_cancel_booking_for_logged_in_user(self):
        """Ensure authenticated users can cancel their booking."""
        self.client.login(username='testuser1', password='password1')
        response = self.client.post(self.url_user1_future)
        self.assertRedirects(response, reverse('my-bookings'))
        self.assertFalse(
            Booking.objects.filter(id=self.booking_future.id).exists(),
            "Booking was not deleted as expected."
        )

    def test_user2_cannot_cancel_other_user_booking(self):
        """Ensure a user cannot cancel another user's booking."""
        # Login as user2 (not the owner of the booking)
        self.client.login(username='testuser2', password='password2')

        # Try to cancel user1's booking
        response = self.client.post(self.url_user1_future)

        # Assert that user2 cannot cancel the past booking
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())

    def test_cancel_past_booking(self):
        """Ensure users cannot cancel a past booking."""
        # Login as user1 (the owner of the booking)
        self.client.login(username='testuser1', password='password1')

        # Try to cancel the past booking
        response = self.client.post(self.url_user1_past)

        # Assert that the booking is not canceled
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my-bookings'))
        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())
