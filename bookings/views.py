from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from community_centre.models import CommunityCentre
from .models import TimeSlot, Booking
from .forms import BookingForm
from bookings.utils import is_time_slot_valid_and_available

# Create your views here.

# get the only Community Centre currently
community_centre = CommunityCentre.objects.first()

def time_slot_view(request, booking_slug=None):
    """Display time slots for a limited range of days, starting from tomorrow."""
    today = timezone.now().date()  # Get today's date
    start_date = today + timedelta(days=1)  # Start from tomorrow

    # Get the day offset from the URL parameters (default is 0)
    day_offset = int(request.GET.get('day_offset', 0))  # 0 for the first range, +N for subsequent ranges

    # Set the number of days to display per range
    days_per_page = 10
    display_start = start_date + timedelta(days=day_offset * days_per_page)
    display_end = display_start + timedelta(days=days_per_page - 1)

    # Fetch time slots in the current range
    time_slots = TimeSlot.objects.filter(date__range=[display_start, display_end]).order_by('date', 'start_time')

    # Group time slots by day
    slots_by_day = {}
    current_day = display_start
    while current_day <= display_end:
        slots_for_day = time_slots.filter(date=current_day)
        slots_with_bookings = []

        for slot in slots_for_day:
            has_booking = hasattr(slot, 'booking')  # Check if the slot has a related booking
            slots_with_bookings.append({
                'slot': slot,
                'has_booking': has_booking
            })

        slots_by_day[current_day] = slots_with_bookings
        current_day += timedelta(days=1)

    # Handle form submission (time slot selection)
    if request.method == 'POST':
        selected_slot_id = request.POST.get('time_slot')
        time_slot = get_object_or_404(TimeSlot, id=selected_slot_id)

        if booking_slug:
            # Edit existing booking
            booking = get_object_or_404(Booking, slug=booking_slug)
            return redirect('edit-booking', slug=booking.slug, slot_id=selected_slot_id)

        if selected_slot_id:
            # Save the booking or perform other actions
            return redirect('create-booking', time_slot_id=selected_slot_id)

    booking = None
    if booking_slug:
        booking = get_object_or_404(Booking, slug=booking_slug)
        if request.user != booking.user:
            messages.error(request, "You are not authorized to edit this booking.")
            return redirect('home')  # Redirect to a safe page
    
    context = {
        'slots_by_day': slots_by_day,
        'display_start': display_start,
        'display_end': display_end,
        'day_offset': day_offset,
        'days_per_page': days_per_page,
        'today': today,
        'booking': booking,
    }

    return render(request, 'bookings/timeslot_list.html', context)



@login_required
def create_booking_view(request, time_slot_id):
    """Handle booking creation for a selected time slot."""
    time_slot = get_object_or_404(TimeSlot, id=time_slot_id)

    # Validate the time slot
    is_valid, error_message = is_time_slot_valid_and_available(time_slot)
    if not is_valid:
        messages.error(request, error_message)
        return redirect('time_slots')  # Redirect back to time slots
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Associate the booking with the logged-in user
            booking.time_slot = time_slot
            booking.community_centre = community_centre
            print(booking)
            booking.save()
            messages.success(request, "Booking successfully created.")
            return redirect('my-bookings')  # Redirect to My Bookings page

    else:
        form = BookingForm(initial={'time_slot': time_slot})

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'time_slot': time_slot,
    })

@login_required
def my_bookings_view(request):
    """Display the user's bookings and allow editing or cancellation."""
    # Get the current user
    user = request.user

    # Fetch the bookings made by the logged-in user
    user_bookings = Booking.objects.filter(user=user).order_by('time_slot')  # You can order by booking creation date

    # Get current datetime
    current_datetime = timezone.now()

    # Separate past and upcoming bookings
    past_bookings = []
    upcoming_bookings = []

    for booking in user_bookings:
        # Combine date and time to create naive datetime
        booking_start_naive = datetime.combine(booking.time_slot.date, booking.time_slot.start_time)
        booking_end_naive = datetime.combine(booking.time_slot.date, booking.time_slot.end_time)

        # Make the combined datetimes timezone-aware
        booking_start = timezone.make_aware(booking_start_naive)
        booking_end = timezone.make_aware(booking_end_naive)

        # Categorize as past or upcoming based on the current datetime
        if booking_end < current_datetime:
            past_bookings.append(booking)
        else:
            upcoming_bookings.append(booking)

    context = {
        'past_bookings': past_bookings,
        'upcoming_bookings': upcoming_bookings
    }

    return render(request, 'bookings/my_bookings.html', context)

@login_required
def cancel_booking(request, slug):
    """Cancel an existing booking."""
    # Get the booking object by ID
    booking = get_object_or_404(Booking, slug=slug)

    if (request.user == booking.user):

        # Ensure that the booking is not in the past (optional)
        if booking.time_slot.date < timezone.now().date():
            return render(request, 'bookings/booking_error.html', {
                'message': 'You cannot cancel bookings in the past.'
            })

        # Cancel the booking (delete it)
        booking.delete()
        messages.success(request, "Booking successfully deleted.")
        return redirect('my-bookings')  # Redirect to the user's bookings page
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('home')  # Redirect to a safe page

@login_required
def edit_booking_view(request, slug, slot_id=None):
    """Edit an existing booking."""
    # Retrieve the booking
    booking = get_object_or_404(Booking, slug=slug)

    if (request.user == booking.user):

        # Retrieve the new time slot if provided
        new_time_slot = get_object_or_404(TimeSlot, id=slot_id) if slot_id else None
        
        if new_time_slot:

            # Validate the new time slot
            is_valid, error_message = is_time_slot_valid_and_available(new_time_slot, exclude_booking_id=booking.id)
            if not is_valid:
                messages.error(request, error_message)
                return redirect('time_slots', booking_slug=booking.slug)

        # Handle form submission
        if request.method == 'POST':
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                booking = form.save(commit=False)
                if new_time_slot:
                    booking.time_slot = new_time_slot
                booking.save()
                messages.success(request, "Booking successfully updated.")
                return redirect('my-bookings')
        else:
            form = BookingForm(instance=booking)

        return render(request, 'bookings/edit_booking.html', {
            'form': form,
            'booking': booking,
            'new_time_slot': new_time_slot,
        })
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('home')  # Redirect to a safe page

@login_required
def change_time_slot_view(request, booking_slug):
    """Redirect to the time slots view with the booking slug."""
    booking = get_object_or_404(Booking, slug=booking_slug)

    if (request.user == booking.user):
        return redirect('time_slots', booking_slug=booking_slug)
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('home')  # Redirect to a safe page
