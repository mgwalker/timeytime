from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.shortcuts import render

from backend.models import Client, Entry
from backend.util import WEEKDAYS, get_tz_entry, seconds_to_duration


def index(request):
    if request.user.is_authenticated:
        clients = Client.objects.filter(owner=request.user)

        # Get the active entry for this user. The active entry is
        # the msot recent edit of an entry without an ending time.
        active = Entry.objects.filter(
            client__owner=request.user, end_time=None, editedto=None
        ).first()

        # Identify the first day of the current week. For our
        # purposes, weeks start on Sunday. If the current day
        # is Sunday, it is the first day of the current week.
        start_of_week = (
            datetime.now()
            .astimezone(ZoneInfo("America/Chicago"))
            .replace(hour=0, minute=0, second=0, microsecond=0)
        )
        # Sunday is the 7th day in Python datetime, so we
        # only need to adjust the other days.
        if(start_of_week.weekday() < 6):
            # Since Monday is day 0 but we're looking for
            # Sunday, we need to remvoe an extra day in
            # the time delta (hence the +1 in the time
            # delta creation).
            start_of_week -= timedelta(days=start_of_week.weekday() + 1)

        entries = (
            Entry.objects.filter(
                client__owner=request.user,     # Only this user's entries
                start_time__gte=start_of_week,  # Only this week's entries
                deleted=False,                  # Only undeleted entries
                editedto=None,                  # The most recent edit of entries
            )
            .order_by("start_time")
            .reverse()
        )

        # This dictionary is used to display the individual entities
        # for each day of the current week.
        days = {}

        # This dictionary is used to roll up today's summary.
        today = {}

        # This dictionary is used to roll up the weekly summary.
        week = {}

        for entry in entries:
            # Get times in client timezone, plus formatted duration
            entry = get_tz_entry(entry)

            # Now get midnight of the current day in the client timezone.
            start_of_day = datetime.now()
            if entry.client.timezone:
                start_of_day = datetime.now(tz=ZoneInfo(entry.client.timezone))
            start_of_day = start_of_day.replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            # WHAT DAY IS IT
            dow = WEEKDAYS[entry.start_time.weekday()]

            # Add this client to the week if we don't already
            # have it, and then associate this entry with its
            # client.
            if entry.client not in week:
                week[entry.client] = []
            week[entry.client].append(entry)

            # Likewise for days, associate entries with the
            # weekday on which they were worked.
            if dow not in days:
                days[dow] = []
            days[dow].append(entry)

            # If an entry's start time is after midnight of
            # the current day, relative to the client timezone,
            # then it belongs to today.
            if entry.start_time > start_of_day:
                # If the client has not already been
                # recorded today, add it.
                if entry.client.name not in today:
                    today[entry.client.name] = {
                        "time": 0,
                        "client": entry.client,
                    }

                if entry.end_time:
                    # If the entry has an end time, then we can add
                    # its duration to the total client duration for
                    # today.
                    today[entry.client.name]["time"] += (
                        entry.end_time - entry.start_time
                    ).total_seconds()
                else:
                    # Otherwise, the entry is active. Set the active
                    # time to the entry's start time, and we'll use
                    # that to compute the dynamic portion of the
                    # total duration. (That is, the duration of
                    # the finished entries plus the ongoing duration
                    # of the active entry.)
                    today[entry.client.name]["active"] = entry.start_time

        # If there are no active timers for today, we can go ahead
        # and format the total duration into a nice string. Otherwise
        # it'll need to be done on the client side.
        for times in today.values():
            if "active" not in times:
                times["time"] = seconds_to_duration(times["time"])

        # Prepare the data to be more easily consumed by templates.
        week = [
            {
                "active": active in week[client],
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

        # For entries that are finished, format the total duration.
        # Otherwise, set the "from" time so it can be computed
        # dynamically on the frontend.
        for item in week:
            item["time"] = sum(item["time"])
            if item["active"]:
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
