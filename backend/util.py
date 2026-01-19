from zoneinfo import ZoneInfo


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
        return f"{hours}:{minutes:02d}"
    return f"{minutes} minutes"


def get_entry_duration(entry):
    if entry.end_time:
        seconds = (entry.end_time - entry.start_time).total_seconds()
        hours = int(seconds / 3600)
        seconds -= hours * 3600
        minutes = int(seconds / 60)

        if hours:
            return f"{hours}:{minutes:02d}"
        return f"{minutes} minutes"
    return None
