from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta
from bookings.models import TimeSlot, Booking, User
from community_centre.models import CommunityCentre


class TimeSlotViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        # Create test users
        cls.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        cls.other_user = User.objects.create_user(
            username='otheruser', password='password456'
        )

        # Create a CommunityCentre instance
        cls.community_centre = CommunityCentre.objects.create(
            name='Evergreen Community Centre',
            description='A community space for all types of events.',
            address='123 Evergreen St.',
            operating_start_day=1,
            operating_end_day=5,
            opening_time='09:00:00',
            closing_time='17:00:00'
        )

        # Create test time slots for the next 15 days
        today = now().date()
        cls.time_slots = []
        for i in range(15):
            slot = TimeSlot.objects.create(
                community_centre=cls.community_centre,
                date=today + timedelta(days=i + 1),
                start_time="10:00:00",
                end_time="12:00:00"
            )
            cls.time_slots.append(slot)

        # Create a test booking for one time slot
        cls.booking = Booking.objects.create(
            user=cls.user,
            time_slot=cls.time_slots[0],
            community_centre=cls.community_centre,
            occasion="Test Occasion",
            occasion_type="public",
            notes="This is a test booking."
        )

    def test_view_time_slots_unauthenticated(self):
        """Test that unauthenticated users can view time slots"""
        response = self.client.get(reverse('time_slots'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/timeslot_list.html')
        self.assertIn('slots_by_day', response.context)

    def test_view_time_slots_authenticated(self):
        """Test that authenticated users can view time slots"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('time_slots'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/timeslot_list.html')
        self.assertIn('slots_by_day', response.context)

    def test_pagination_time_slots(self):
        """Test time slot pagination works correctly"""
        response = self.client.get(reverse('time_slots') + '?day_offset=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('display_start', response.context)
        self.assertIn('display_end', response.context)

    def test_edit_booking_view(self):
        """Test editing a booking with valid slug"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('time_slots', kwargs={'booking_slug': self.booking.slug}),
            {'time_slot': self.time_slots[1].id}
        )
        self.assertRedirects(response, reverse('edit-booking', kwargs={
            'slug': self.booking.slug,
            'slot_id': self.time_slots[1].id
        }))

    def test_unauthorized_edit_booking(self):
        """Test unauthorized access to editing a booking"""
        self.client.login(username='otheruser', password='password456')
        response = self.client.get(
            reverse(
                'time_slots',
                kwargs={'booking_slug': self.booking.slug}
            )
        )
        self.assertRedirects(response, reverse('home'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            "You are not authorized to edit this booking."
        )

    def test_post_new_booking(self):
        """Test creating a new booking by selecting a time slot"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('time_slots'), {
            'time_slot': self.time_slots[2].id
        })
        self.assertRedirects(response, reverse('create-booking', kwargs={
            'time_slot_id': self.time_slots[2].id
        }))

    def test_slots_displayed_correctly(self):
        """Test that time slots are grouped and displayed by day"""
        response = self.client.get(reverse('time_slots'))
        slots_by_day = response.context['slots_by_day']
        self.assertTrue(slots_by_day)
        for day, slots in slots_by_day.items():
            self.assertTrue(all(
                isinstance(slot['slot'], TimeSlot) for slot in slots
            ))
