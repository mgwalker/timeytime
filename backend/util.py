from datetime import datetime
from zoneinfo import ZoneInfo
import os

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


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


def isto_quick_timestamp():
    tz = ZoneInfo("America/Chicago")
    now = datetime.now(tz=tz)

    # The offset expected by the form is minutes from UTC. And weirdly,
    # it expects POSITIVE numbers for timezones behind UTC and NEGATIVE
    # numbers for timezones ahead of UTC. Bass-ackwards, as they say.
    tzoffset = -(tz.utcoffset(now).total_seconds() / 60)

    username = os.environ.get("ISTO_USERNAME")
    password = os.environ.get("ISTO_PASSWORD")

    if not username or not password:
        return

    timestamp = now.strftime("%-m/%-d/%Y %-I:%M:%S %p")

    smagentname = "tlmisi2-prod-dc2prisivag0013-1"

    url = f"https://tlmisi2.adp.com/adptlmqts/Private/quickTSprivate.aspx?TimeZoneOffset={tzoffset}&TimeStamp={timestamp}&BrowserTime={timestamp}&USER={username}&PASSWORD={password}&smagentname={smagentname}"
