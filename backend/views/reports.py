from datetime import timedelta
from itertools import groupby

from django.shortcuts import redirect, render

from backend.models import Entry
from backend.util import (
    get_entry_duration,
    get_tz_entry,
    get_week_dates,
    seconds_to_duration,
)


def reports(request):
    if request.user.is_authenticated:
        past = request.GET.get("past", 0)
        try:
            past = int(past)
        except ValueError:
            past = 0

        (start_of_week, end_of_week) = get_week_dates(past)

        entries = Entry.objects.filter(
            start_time__gt=start_of_week,
            end_time__lt=end_of_week,
            deleted=False,
            editedto=None,
        )

        week = [
            {"entry": get_tz_entry(entry), "duration": get_entry_duration(entry)}
            for entry in entries
        ]

        days = []
        for _, day_entries in groupby(entries, lambda entry: entry.start_time.day):
            day_entries = list(day_entries)

            day_entries.sort(
                key=lambda e: e.client.name,
            )

            day = {
                "day": day_entries[0].start_time,
                "clients": [],
            }
            days.append(day)

            for _, client_entries in groupby(
                day_entries, lambda entry: entry.client.name
            ):
                client_entries = list(client_entries)
                client = {
                    "name": client_entries[0].client.name,
                    "color": client_entries[0].client.color,
                    "duration": seconds_to_duration(
                        sum(
                            [
                                (entry.end_time - entry.start_time).total_seconds()
                                for entry in client_entries
                            ]
                        )
                    ),
                }
                day["clients"].append(client)

        return render(
            request,
            "reports.html",
            {
                "past": past,
                "start_of_week": start_of_week,
                "end_of_week": end_of_week - timedelta(days=1),
                "entries": week,
                "days": days,
            },
        )
    return redirect("index")
