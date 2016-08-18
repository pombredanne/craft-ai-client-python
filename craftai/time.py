import six
import time as _time

from datetime import datetime
from datetime import tzinfo
from pytz import utc as pyutc
from tzlocal import get_localzone

from craftai.errors import CraftAITimeError

_EPOCH = datetime(1970, 1, 1, tzinfo=pyutc)
_ISO_FMT = "%Y-%m-%dT%H:%M:%S%z"


class Time(object):
    """Handles time in a useful way for craft ai's client"""
    def __init__(self, t=None, tz=""):
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
                    """Unable to instantiate Time from given timestamp. {}""".
                    format(e.__str__()))
        elif isinstance(t, six.string_types):
            # Else if t is a string we try to interprete it as an ISO time
            # string
            try:
                time = datetime.strptime(t, _ISO_FMT)
            except ValueError as e:
                raise CraftAITimeError(
                    """Unable to instantiate Time from given string. {}""".
                    format(e.__str__()))

        if tz:
            # If a timezone is specified we can try to use it
            if isinstance(tz, tzinfo):
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
                        """Unable to instantiate Time from given timezone."""
                        """ {}""".format(e.__str__()))
            else:
                raise CraftAITimeError(
                    """Unable to instantiate Time with the given timezone."""
                    """ {} is neither a string nor a timezone.""".format(tz)
                )

        try:
            self.utc_iso = time.isoformat()
        except ValueError as e:
            raise CraftAITimeError(
                """Unable to create ISO 8061 UTCstring. {}""".
                format(e.__str__()))

        self.day_of_week = time.weekday()
        self.time_of_day = time.hour + time.minute / 60 + time.second / 3600
        self.timezone = time.strftime("%z")
        self.ts = Time.timestamp_from_datetime(time)

    def to_dict(self):
        """Returns the Time instance as a usable dictionary for craftai"""
        return {
            "timestamp": int(self.ts),
            "timezone": self.timezone,
            "time_of_day": self.time_of_day,
            "day_of_week": self.day_of_week,
            "utc_iso": self.utc_iso
        }

    @staticmethod
    def timestamp_from_datetime(dt):
        """Returns POSIX timestamp as float"""
        if dt.tzinfo is None:
            return _time.mktime((dt.year, dt.month, dt.day, dt.hour, dt.minute,
                                 dt.second, -1, -1, -1)) + dt.microsecond / 1e6
        else:
            return (dt - _EPOCH).total_seconds()
