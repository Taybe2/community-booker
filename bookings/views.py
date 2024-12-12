from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from community_centre.models import CommunityCentre
from .models import TimeSlot, Booking
from .forms import BookingForm
from bookings.utils import is_time_slot_valid_and_available

# Create your views here.

# get the only Community Centre currently
community_centre = CommunityCentre.objects.first()


def time_slot_view(request, booking_slug=None):
    """
    Displays time slots for a limited range of days, starting from tomorrow.

    This view displays a list of available time slots for booking,
    grouped by day, and allows users to either create a new booking
    or edit an existing one.
    The time slots displayed are for a range of days starting from tomorrow,
    with the ability to navigate through multiple pages of time slots using
    the `day_offset` URL parameter.

    **Context**

    ``slots_by_day``
        A dictionary where the key is the date and the value is a list of time
        slots for that date, along with a flag indicating whether the slot has
        an existing booking.

    ``display_start``
        The start date of the current time slot range being displayed.

    ``display_end``
        The end date of the current time slot range being displayed.

    ``day_offset``
        The offset for the day range, which determines which set of days
        to display.

    ``days_per_page``
        The number of days shown per page of time slots.

    ``today``
        The current date (today's date).

    ``booking``
        The booking object :model:`bookings.Booking` that is being edited, if
        the `booking_slug` is provided.

    **Template:**

    :template:`bookings/timeslot_list.html`
    """
    today = timezone.now().date()  # Get today's date
    start_date = today + timedelta(days=1)  # Start from tomorrow

    # Get the day offset from the URL parameters (default is 0)
    day_offset = int(request.GET.get('day_offset', 0))

    # Set the number of days to display per range
    days_per_page = 10
    display_start = start_date + timedelta(days=day_offset * days_per_page)
    display_end = display_start + timedelta(days=days_per_page - 1)

    # Fetch time slots in the current range
    time_slots = TimeSlot.objects.filter(
        date__range=[display_start, display_end]).order_by(
            'date', 'start_time')

    # Group time slots by day
    slots_by_day = {}
    current_day = display_start

    while current_day <= display_end:
        slots_for_day = time_slots.filter(date=current_day)
        slots_with_bookings = []

        for slot in slots_for_day:
            # Check if the slot has a related booking
            has_booking = hasattr(slot, 'booking')
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
            return redirect(
                'edit-booking',
                slug=booking.slug,
                slot_id=selected_slot_id
            )

        if selected_slot_id:
            # Save the booking or perform other actions
            return redirect('create-booking', time_slot_id=selected_slot_id)

    booking = None
    if booking_slug:
        booking = get_object_or_404(Booking, slug=booking_slug)
        if request.user != booking.user:
            messages.error(
                request,
                "You are not authorized to edit this booking.")
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
    """
    Handles the creation of a booking for a selected time slot.

    This view validates the selected time slot, displays a booking form, and
    processes the booking submission. It associates the booking with the
    logged-in user and the selected time slot, and saves the booking to
    the database.

    **Context**

    ``form``
        An instance of :form:`bookings.BookingForm`, pre-filled with the
        selected time slot.

    ``time_slot``
        The time slot that the user is booking. An instance
        of :model:`bookings.TimeSlot`

    **Template:**

    :template:`bookings/create_booking.html`

    **Redirects**

    After a successful booking creation, the user is redirected
    to the 'My Bookings' page. If there is an error with the selected
    time slot (e.g., unavailable), the user is redirected back to
    the time slots page with an error message.
    """
    time_slot = TimeSlot.objects.filter(id=time_slot_id).first()
    
    if not time_slot:
        messages.error(
            request,
            "The selected time slot is invalid or does not exist.")
        return redirect('time_slots')


    # Validate the time slot
    is_valid, error_message = is_time_slot_valid_and_available(time_slot)
    if not is_valid:
        messages.error(request, error_message)
        return redirect('time_slots')  # Redirect back to time slots

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Associate the booking with the logged-in user
            booking.user = request.user

            booking.time_slot = time_slot
            booking.community_centre = community_centre
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
    """
    Display the user's bookings, separated into past and upcoming categories.
    Users can view, edit, or cancel their bookings.

    **Context**

    ``past_bookings``
        A paginated list of the user's past bookings (7 per page).
    ``upcoming_bookings``
        A paginated list of the user's upcoming bookings (7 per page).

    **Template**

    :template:`bookings/my_bookings.html`
    """
    # Get the current user
    user = request.user

    # Fetch the bookings made by the logged-in user
    user_bookings = Booking.objects.filter(
        user=user).order_by('time_slot')

    # Get current datetime
    current_datetime = timezone.now()

    # Separate past and upcoming bookings
    past_bookings = []
    upcoming_bookings = []

    for booking in user_bookings:
        # Combine date and time to create naive datetime
        booking_start_naive = datetime.combine(
            booking.time_slot.date,
            booking.time_slot.start_time)
        booking_end_naive = datetime.combine(
            booking.time_slot.date,
            booking.time_slot.end_time)

        # Make the combined datetimes timezone-aware
        booking_start = timezone.make_aware(booking_start_naive)
        booking_end = timezone.make_aware(booking_end_naive)

        # Categorize as past or upcoming based on the current datetime
        if booking_end < current_datetime:
            past_bookings.append(booking)
        else:
            upcoming_bookings.append(booking)

    # Show 7 past bookings per page
    past_paginator = Paginator(past_bookings, 7)

    # Show 7 upcoming bookings per page
    upcoming_paginator = Paginator(upcoming_bookings, 7)

    past_page_number = request.GET.get('past_page', 1)
    upcoming_page_number = request.GET.get('upcoming_page', 1)

    past_page_obj = past_paginator.get_page(past_page_number)
    upcoming_page_obj = upcoming_paginator.get_page(upcoming_page_number)

    context = {
        'past_bookings': past_page_obj,
        'upcoming_bookings': upcoming_page_obj,
    }

    return render(request, 'bookings/my_bookings.html', context)


@login_required
def cancel_booking(request, slug):
    """
    Cancel an existing booking if it belongs to the logged-in user
    and is not in the past.

    **Context**

    ``booking``
        An instance of :model:`bookings.Booking`.

    **Behavior**

    - If the booking is in the past:
      Displays an error message and redirects to :view:`my_bookings_view`.
    - If the booking belongs to another user:
      Displays an error message and redirects to :view:`home`.
    - If the booking is valid for cancellation:
      Deletes the booking, displays a success message,
      and redirects to :view:`my_bookings_view`.
    """
    # Get the booking object by ID
    #booking = get_object_or_404(Booking, slug=slug)
    booking = Booking.objects.filter(slug=slug).first()

    if not booking:
        messages.error(
            request,
            "This booking is invalid or does not exist.")
        return redirect('my-bookings')

    if (request.user == booking.user):
        time_slot = booking.time_slot

        # Validate the time slot
        is_valid, error_message = is_time_slot_valid_and_available(
            time_slot, exclude_booking_id=booking.id
        )

        if not is_valid:
            messages.error(request, error_message)
            return redirect('my-bookings')

        # Cancel the booking (delete it)
        booking.delete()
        messages.success(request, "Booking successfully deleted.")
        return redirect('my-bookings')  # Redirect to the user's bookings page
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('home')  # Redirect to a safe page


@login_required
def edit_booking_view(request, slug, slot_id=None):
    """
    Handle editing an existing booking.

    Users can update their booking details or change the associated time slot
    if a valid new time slot ID is provided.

    **Parameters:**

    - `slug`: The unique identifier for the booking to be edited.
    - `slot_id` (optional): The ID of a new time slot to update the booking to.

    **Context:**

    - `form`: A pre-filled instance of :form:`BookingForm` for
    editing the booking.
    - `booking`: The :model:`Booking` instance being edited.
    - `new_time_slot`: The :model:`TimeSlot` instance being updated to,
    if applicable.

    **Logic:**

    - Validates if the logged-in user is authorized to edit the specified
    booking.
    - If a new time slot ID is provided:
        - Checks its validity and availability, excluding the current booking.
        - Displays an error message if the slot is invalid.
    - Processes form submission to update the booking details.
    - If successful, updates the booking and redirects to `my-bookings`.

    **Permissions:**

    - Only the user who created the booking can edit it. Unauthorized access
      results in an error message and a redirect to the home page.

    **Template:**

    :template:`bookings/edit_booking.html`
    """
    # Retrieve the booking
    #booking = get_object_or_404(Booking, slug=slug)
    booking = Booking.objects.filter(slug=slug).first()

    if not booking:
        messages.error(
            request,
            "This booking is invalid or does not exist.")
        return redirect('my-bookings')

    if (request.user == booking.user):
        time_slot = booking.time_slot

        # Validate the time slot
        is_valid, error_message = is_time_slot_valid_and_available(
            time_slot, exclude_booking_id=booking.id
        )

        if not is_valid:
            messages.error(request, error_message)
            return redirect('my-bookings')

        new_time_slot = None

        if slot_id:
            new_time_slot = TimeSlot.objects.filter(id=slot_id).first()
            if not new_time_slot:
                messages.error(
                    request,
                    "The selected time slot is invalid or does not exist.")
                return redirect('time_slots', booking_slug=booking.slug)

            # Validate the new time slot
            is_valid, error_message = is_time_slot_valid_and_available(
                new_time_slot, exclude_booking_id=booking.id
            )
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
    """
    Redirect the user to the time slots view to select a new time slot
    for an existing booking.

    **Parameters:**

    - `booking_slug`: The unique identifier for the booking whose time slot
    is to be changed.

    **Logic:**

    - Validates if the logged-in user is authorized to change the time slot
    for the specified booking.
    - If authorized:
        - Redirects the user to the time slots view with the booking slug
        passed as a parameter.
    - If unauthorized:
        - Displays an error message and redirects the user to the home page.

    **Permissions:**

    - Only the user who created the booking can change its time slot.
    Unauthorized access results in an error message and a redirect
    to the home page.

    **Redirects:**

    - To `time_slots` view with `booking_slug` if the user is authorized.
    - To `home` if the user is not authorized.
    """
    booking = get_object_or_404(Booking, slug=booking_slug)

    if (request.user == booking.user):
        return redirect('time_slots', booking_slug=booking_slug)
    else:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('home')  # Redirect to a safe page
