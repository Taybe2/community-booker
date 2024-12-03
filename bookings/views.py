from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from community_centre.models import CommunityCentre
from .models import TimeSlot, Booking
from .forms import BookingForm

# Create your views here.

# get the only Community Centre currently
community_centre = CommunityCentre.objects.first()

def time_slot_view(request, booking_slug=None):
    """Display time slots for the current week or other weeks, with all days accounted for."""

    today = timezone.now().date()  # Get today's date

    # Get the week offset from the URL parameters (default is 0)
    week_offset = int(request.GET.get('week_offset', 0))  # 0 for the current week, +1 for next week, -1 for previous week

    # Weeks always start from Monday
    week_start = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)

    # Calculate the end of the week (Sunday)
    week_end = week_start + timedelta(days=6)  # End of the week (Sunday)

    # Fetch all time slots between week_start and week_end
    time_slots = TimeSlot.objects.filter(date__range=[week_start, week_end]).order_by('date', 'start_time')

    # Group time slots by day
    slots_by_day = {}
    current_day = week_start
    while current_day <= week_end:
        slots_for_day = time_slots.filter(date=current_day)
        slots_with_bookings = []
        time_slot = TimeSlot.objects.first()

        # Check each time slot for bookings
        for slot in slots_for_day:
            try:
                # Try to access the related 'booking'
                slot.booking  # If no booking exists, this will raise RelatedObjectDoesNotExist
                has_booking = True
            except:
                has_booking = False
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
            booking.time_slot = time_slot
            booking.save()
            messages.success(request, "Time slot successfully updated.")
            return redirect('edit-booking', slug=booking.slug)
        
        if selected_slot_id:
            # Save the booking in the database or perform other actions
            return redirect('create-booking', time_slot_id=selected_slot_id)
    
    booking = None
    if booking_slug:
        booking = get_object_or_404(Booking, slug=booking_slug)
        if (request.user != booking.user):
            messages.error(request, "You are not authorized to edit this booking.")
            return redirect('home')  # Redirect to a safe page

    context = {
        'slots_by_day': slots_by_day,
        'week_start': week_start,
        'week_end': week_end,
        'week_offset': week_offset,
        'today': today,
        'booking': booking,
    }

    return render(request, 'bookings/timeslot_list.html', context)


@login_required
def create_booking_view(request, time_slot_id):
    """Handle booking creation for a selected time slot."""
    time_slot = get_object_or_404(TimeSlot, id=time_slot_id)

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
        return redirect('my-bookings')  # Redirect to a safe page

@login_required
def edit_booking_view(request, slug):
    """Edit an existing booking."""
    booking = get_object_or_404(Booking, slug=slug)

    if (request.user == booking.user):

        if request.method == 'POST':
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()  # Save the updated booking
                messages.success(request, "Booking successfully updated.")
                return redirect('my-bookings')
        else:
            form = BookingForm(instance=booking)

        return render(request, 'bookings/edit_booking.html', {
            'form': form,
            'booking': booking
        })
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('my-bookings')  # Redirect to a safe page

@login_required
def change_time_slot_view(request, booking_slug):
    """Redirect to the time slots view with the booking slug."""
    booking = get_object_or_404(Booking, slug=booking_slug)

    if (request.user == booking.user):
        return redirect('time_slots', booking_slug=booking_slug)
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('home')  # Redirect to a safe page
