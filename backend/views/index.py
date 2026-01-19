from django.shortcuts import render
from backend.models import Client, Entry
from datetime import datetime
from zoneinfo import ZoneInfo
from backend.util import (
    get_entry_duration,
    get_entry_end_time,
    get_entry_start_time,
    seconds_to_duration,
)


def index(request):
    if request.user.is_authenticated:
        clients = Client.objects.filter(owner=request.user)
        active = Entry.objects.filter(client__owner=request.user, end_time=None).first()

        entries = (
            Entry.objects.filter(client__owner=request.user)
            .order_by("start_time")
            .reverse()
        )

        today = {}
        for entry in entries:
            start_of_day = datetime.now()
            if entry.client.timezone:
                start_of_day = datetime.now(tz=ZoneInfo(entry.client.timezone))
            start_of_day = start_of_day.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            if entry.start_time > start_of_day:
                if entry.end_time:
                    if entry.client.name not in today:
                        today[entry.client.name] = {
                            "time": 0,
                            "client": entry.client,
                        }
                    today[entry.client.name]["time"] += (
                        get_entry_end_time(entry) - get_entry_start_time(entry)
                    ).total_seconds()
                else:
                    if entry.client.name not in today:
                        today[entry.client.name] = {
                            "time": 0,
                            "active": "",
                            "client": entry.client,
                        }
                    today[entry.client.name]["active"] = get_entry_start_time(entry)

        for times in today.values():
            if "active" not in times:
                times["time"] = seconds_to_duration(times["time"])

        entries = [
            {
                "id": entry.id,
                "start_time": get_entry_start_time(entry),
                "end_time": get_entry_end_time(entry),
                "duration": get_entry_duration(entry),
                "note": entry.note,
                "client": entry.client,
            }
            for entry in entries
        ]

        return render(
            request,
            "index.auth.html",
            {
                "active": active,
                "clients": clients,
                "entries": entries,
                "today": today,
            },
        )
    return render(request, "index.html")
