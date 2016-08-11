import six
import time as _time

from datetime import datetime
from pytz import timezone as _timezone
from pytz import utc as pyutc
from tzlocal import get_localzone

from craftai.errors import CraftAITimeError

_EPOCH = datetime(1970, 1, 1, tzinfo=pyutc)
_ISO_FMT = "%Y-%m-%dT%H-%M:%S%z"


def create_time(t=None, tz=""):
    if not t:
        # If no initial timestamp is given, the current local time is used
        time = datetime.now(get_localzone())
    elif isinstance(t, int):
        # Else if t is an int we try to use it as a given timestamp with
        # local UTC offset by default
        try:
            time = datetime.fromtimestamp(t, get_localzone())
        except (OverflowError, OSError) as e:
            raise CraftAITimeError(
                """Unable to create time object from given timestamp. {}""".
                format(e.__str__()))
    elif isinstance(t, six.string_types):
        # Else if t is a string we try to interprete it as an ISO time string
        try:
            time = datetime.strptime(t, _ISO_FMT)
        except ValueError as e:
            raise CraftAITimeError(
                """Unable to create time object from given string. {}""".
                format(e.__str__()))

    if tz:
        # If a timezone is specified we can try to use it
        if isinstance(tz, _timezone):
            # If it's already a timezone object, no more work is needed
            time = time.astimezone(tz)
        elif isinstance(tz, six.string_types):
            # If it's a string, we convert it to a usable timezone object
            tz = tz.replace(":", "")
            try:
                temp_dt = datetime.strptime(tz, "%z")
                time = time.astimezone(temp_dt.tzinfo)
            except ValueError as e:
                raise CraftAITimeError(
                    """Unable to create time object from given timezone. {}""".
                    format(e.__str__()))
        else:
            raise CraftAITimeError(
                """Unable to create a time object with the given timezone."""
                """ {} is neither a string nor a timezone.""".format(tz)
            )

    try:
        utc_iso = time.isoformat()
    except ValueError as e:
        raise CraftAITimeError(
            """Unable to create ISO 8061 UTCstring. {}""".
            format(e.__str__()))

    day_of_week = time.weekday()
    time_of_day = time.hour + time.minute / 60 + time.second / 3600
    timezone = time.strftime("%z")
    ts = timestamp(time)

    return {
        "timestamp": int(ts),
        "timezone": timezone,
        "time_of_day": time_of_day,
        "day_of_week": day_of_week,
        "utc_iso": utc_iso
    }


def timestamp(dt):
    """Return POSIX timestamp as float"""
    if dt.tzinfo is None:
        return _time.mktime((dt.year, dt.month, dt.day, dt.hour, dt.minute,
                             dt.second, -1, -1, -1)) + dt.microsecond / 1e6
    else:
        return (dt - _EPOCH).total_seconds()
