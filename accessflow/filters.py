import datetime as dt

def format_time(time):
    if isinstance(time, dt.timedelta):
        seconds = int(time.total_seconds())
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
    return None

def get_day_with_suffix(day):
    day_suffix = "th"
    if day in [1, 21, 31]:
        day_suffix = "st"
    elif day in [2, 22]:
        day_suffix = "nd"
    elif day in [3, 23]:
        day_suffix = "rd"

    day = str(day)
    if day[0] == "0":
        day = day[1:]

    return day + day_suffix

def format_date(date):
    if isinstance(date, dt.datetime):
        return date.strftime(f"{get_day_with_suffix(date.day)} %b %Y")
    return None
    
def format_datetime(datetime):
    if isinstance(datetime, dt.datetime):
        hour = datetime.strftime("%I")
        if hour[0] == "0":
            hour = hour[1:]
        return datetime.strftime(f"{get_day_with_suffix(datetime.day)} %B %Y at {hour}:%M %p")
    return None