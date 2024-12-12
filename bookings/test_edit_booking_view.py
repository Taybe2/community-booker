from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from community_centre.models import CommunityCentre
from bookings.models import Booking, TimeSlot


class TestEditBookingView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.other_user = User.objects.create_user(
            username='otheruser', password='password')
        self.community_centre = CommunityCentre.objects.create(
            name='Evergreen Community Centre',
            description='Community space',
            address='123 Evergreen St.',
            operating_start_day=1,
            operating_end_day=5,
            opening_time='09:00:00',
            closing_time='17:00:00'
        )
        self.time_slot = TimeSlot.objects.create(
            date='2024-12-15',
            start_time='10:00:00',
            end_time='11:00:00',
            community_centre=self.community_centre
        )
        self.booking = Booking.objects.create(
            user=self.user,
            time_slot=self.time_slot,
            community_centre=self.community_centre,
            occasion="Meeting",
            occasion_type="private",
            notes="Test booking"
        )
        self.url = reverse('edit-booking', args=[self.booking.slug])

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_login'), response.url)

    def test_access_denied_for_other_users(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(self.url)

        # Check for a redirect to the home page
        self.assertRedirects(response, reverse('home'))

        # Check if the error message is present
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("You are not authorized to edit this booking." in str(msg) for msg in messages),
            "Expected 'You are not authorized' message not found"
        )

    def test_shows_form_for_owner(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Booking")

    def test_valid_post_updates_booking(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {
            'occasion': 'Updated Event',
            'occasion_type': 'public',
            'notes': 'Updated notes'
        })
        self.assertRedirects(response, reverse('my-bookings'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.occasion, 'Updated Event')
        self.assertEqual(self.booking.occasion_type, 'public')
        self.assertEqual(self.booking.notes, 'Updated notes')

    def test_invalid_post_displays_errors(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {
            'occasion': '',
            'occasion_type': 'public',
            'notes': 'Updated notes'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            'occasion',
            'This field is required.'
        )

    def test_invalid_slot_id(self):
        invalid_url = reverse('edit-booking', args=[self.booking.slug, 999])
        self.client.login(username='testuser', password='password')
        response = self.client.get(invalid_url)
        self.assertRedirects(
            response, reverse('time_slots', args=[self.booking.slug]))
