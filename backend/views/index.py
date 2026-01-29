from django.shortcuts import render
from backend.models import Client, Entry
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from backend.util import seconds_to_duration, get_tz_entry, WEEKDAYS


def index(request):
    if request.user.is_authenticated:
        clients = Client.objects.filter(owner=request.user)
        active = Entry.objects.filter(client__owner=request.user, end_time=None).first()

        start_of_week = (
            datetime.now()
            .astimezone(ZoneInfo("America/Chicago"))
            .replace(hour=0, minute=0, second=0, microsecond=0)
        )
        start_of_week -= timedelta(days=start_of_week.weekday() + 1)

        entries = (
            Entry.objects.filter(
                client__owner=request.user, start_time__gte=start_of_week
            )
            .order_by("start_time")
            .reverse()
        )

        today = {}
        days = {}
        week = {}

        for entry in entries:
            entry = get_tz_entry(entry)

            start_of_day = datetime.now()
            if entry.client.timezone:
                start_of_day = datetime.now(tz=ZoneInfo(entry.client.timezone))
            start_of_day = start_of_day.replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            dow = WEEKDAYS[entry.start_time.weekday()]

            if dow != "Saturday" or len(days.keys()) == 0:
                if entry.client not in week:
                    week[entry.client] = []
                week[entry.client].append(entry)
                if dow not in days:
                    days[dow] = []
                days[dow].append(entry)

            if entry.start_time > start_of_day:
                if entry.end_time:
                    if entry.client.name not in today:
                        today[entry.client.name] = {
                            "time": 0,
                            "client": entry.client,
                        }
                    today[entry.client.name]["time"] += (
                        entry.end_time - entry.start_time
                    ).total_seconds()
                else:
                    if entry.client.name not in today:
                        today[entry.client.name] = {
                            "time": 0,
                            "active": "",
                            "client": entry.client,
                        }
                    today[entry.client.name]["active"] = entry.start_time

        for times in today.values():
            if "active" not in times:
                times["time"] = seconds_to_duration(times["time"])

        week = [
            {
                "active": False,
                "client": client,
                "entries": week[client],
                "time": [
                    (entry.end_time - entry.start_time).total_seconds()
                    for entry in week[client]
                    if entry.end_time
                ],
            }
            for client in week
        ]

        for item in week:
            item["time"] = sum(item["time"])
            active = next(
                (entry for entry in item["entries"] if not entry.end_time), None
            )
            if active:
                item["active"] = True
                item["from"] = active.start_time
            else:
                item["time"] = seconds_to_duration(item["time"])

        return render(
            request,
            "index.auth.html",
            {
                "active": active,
                "clients": clients,
                "days": days,
                "today": today,
                "week": week,
            },
        )
    return render(request, "index.html")
