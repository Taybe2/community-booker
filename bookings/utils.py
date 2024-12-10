from datetime import datetime
from django.utils import timezone


def is_time_slot_valid_and_available(time_slot, exclude_booking_id=None):
    """
    Check if a given time slot is in the past or is already reserved.
    Args:
        time_slot (TimeSlot): The time slot to check.
        exclude_booking_id (int, optional): Booking ID to exclude
        from the check (useful for editing).
    Returns:
        bool: False if the time slot is reserved or in the past,
        True otherwise.
        string: Message
    """
    # Check if the time slot is in the past or today
    now = timezone.now()
    slot_datetime = timezone.make_aware(
        datetime.combine(time_slot.date, time_slot.start_time))
    if slot_datetime <= now:
        return False, "Time slot must be in the future."

    # Check if the time slot is reserved
    if hasattr(time_slot, 'booking') and (
            exclude_booking_id is None or
            time_slot.booking.id != exclude_booking_id):
        return False, "Time slot is already reserved."

    return True, None
