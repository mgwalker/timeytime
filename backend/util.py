from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_week_dates():
    start_of_week = (
        datetime.now()
        .astimezone(ZoneInfo("America/Chicago"))
        .replace(hour=0, minute=0, second=0, microsecond=0)
    )
    start_of_week -= timedelta(days=start_of_week.weekday() + 1)
    end_of_week = start_of_week + timedelta(days=7)
    return (start_of_week, end_of_week)


def get_tz_entry(entry):
    entry.start_time = get_entry_start_time(entry)
    entry.end_time = get_entry_end_time(entry)
    entry.duration = get_entry_duration(entry)
    return entry


def get_entry_start_time(entry):
    if entry.start_time and entry.client.timezone:
        return entry.start_time.astimezone(ZoneInfo(entry.client.timezone))
    return entry.start_time


def get_entry_end_time(entry):
    if entry.end_time and entry.client.timezone:
        return entry.end_time.astimezone(ZoneInfo(entry.client.timezone))
    return entry.end_time


def seconds_to_duration(seconds):
    hours = int(seconds / 3600)
    seconds -= hours * 3600
    minutes = int(seconds / 60)

    if hours:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes} minutes"


def get_entry_duration(entry):
    if entry.end_time:
        seconds = (entry.end_time - entry.start_time).total_seconds()
        return seconds_to_duration(seconds)
    return None
