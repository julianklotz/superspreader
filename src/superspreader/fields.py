import datetime
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
        if not value and self.required is True:
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
        desired_type = self.get_target_type()
        if value and not isinstance(value, desired_type):
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
