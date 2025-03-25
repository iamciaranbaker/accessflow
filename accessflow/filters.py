from datetime import timedelta

def format_time(time):
    if isinstance(time, timedelta):
        seconds = int(time.total_seconds())
    else:
        seconds = int(time) # If time is already total seconds

    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    elif seconds < 120:
        return "1 minute"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 7200:
        return "1 hour"
    else:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"