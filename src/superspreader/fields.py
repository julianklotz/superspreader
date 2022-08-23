import datetime
import re
from abc import ABC

from .exceptions import ImproperlyConfigured, ValidationException
from .i18n import translate as _


class BaseField(ABC):
    target_type = None

    def __init__(self, source, required=True):
        self.source = source
        self.required = required
        self.locale = None

    def __call__(self, value, locale):
        self.locale = locale
        if value is None and self.required is True:
            msg = _("field.is_required", params={"field": self.source})
            raise ValidationException(msg)

        return self.clean(value)

    def get_target_type(self):
        if self.target_type is None:
            raise ImproperlyConfigured(
                f"You have to specify a target type for {self.__class__.__name__}"
            )
        return self.target_type

    def clean(self, value):
        if value is None:
            return

        desired_type = self.get_target_type()

        if not isinstance(value, desired_type):
            try:
                value = desired_type(value)
            except ValueError:
                msg = _(
                    "field.wrong_type",
                    params={
                        "field": self.source,
                        "target_type": self.get_target_type().__name__,
                        "actual_type": value.__class__.__name__,
                    },
                )
                raise ValidationException(msg)

        return value


class CharField(BaseField):
    target_type = str


class DateField(BaseField):
    target_type = datetime.date

    def clean(self, value):
        if isinstance(value, datetime.datetime):
            value = value.date()

        return super().clean(value)


class DateTimeField(BaseField):
    target_type = datetime.datetime


class FloatField(BaseField):
    target_type = float


class IntegerField(BaseField):
    target_type = int


class TimecodeField(FloatField):
    """
    Parse timecode values like 00:13:06,9 to float value. This is commonly
    used in video and audio processing.
    """

    def clean(self, value):
        if isinstance(value, str):
            value = self.duration_to_seconds(value)

        return super().clean(value)

    def duration_to_seconds(self, duration_string):
        duration_string = duration_string.strip()
        duration_regex = re.compile(r"^(\d{1,2}):(\d{1,2}):(\d{1,2})([-,](\d))?$")
        matches = duration_regex.match(duration_string)

        try:
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
            seconds = int(matches.group(3))

            millis = matches.group(5)
            if millis:
                millis = int(millis)
            else:
                millis = 0
        except Exception:
            msg = _(
                "field.timecode_parse_error",
                params={"timecode": duration_string, "field": self.source},
            )
            raise ValidationException(msg)

        seconds = hours * 3600 + minutes * 60 + seconds + millis / 10

        return seconds
