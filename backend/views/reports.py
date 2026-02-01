from datetime import timedelta

from django.shortcuts import redirect, render

from backend.models import Entry
from backend.util import get_entry_duration, get_tz_entry, get_week_dates


def reports(request):
    if request.user.is_authenticated:
        (start_of_week, end_of_week) = get_week_dates()

        week = [
            {"entry": get_tz_entry(entry), "duration": get_entry_duration(entry)}
            for entry in Entry.objects.filter(
                start_time__gt=start_of_week,
                end_time__lt=end_of_week,
                deleted=False,
                editedto=None,
            )
        ]

        return render(
            request,
            "reports.html",
            {
                "start_of_week": start_of_week,
                "end_of_week": end_of_week - timedelta(days=1),
                "entries": week,
            },
        )
    return redirect("index")
