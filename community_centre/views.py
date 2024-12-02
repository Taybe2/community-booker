from datetime import datetime, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import CommunityCentre
from .utils import generate_time_slots

# Create your views here.


@staff_member_required
def generate_time_slots_view(request, centre_id):
    """View to generate time slots for a specific community center."""
    centre = get_object_or_404(CommunityCentre, pk=centre_id)
    
    if request.method == "POST":
        # Get the user-specified start and end dates
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert them to datetime.date objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        generate_time_slots(centre, start_date, end_date, slot_duration_minutes=60)
        messages.success(request, f"Time slots for {centre.name} were successfully generated.")
        return redirect('admin:community_centre_communitycentre_changelist')  # Redirect to admin list
    
    return render(request, 'community_centre/generate_time_slots.html', {'centre': centre})
