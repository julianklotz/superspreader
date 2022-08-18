import datetime
from abc import ABC

from .exceptions import ImproperlyConfigured, ValidationException


class BaseField(ABC):
    target_type = None

    def __init__(self, source, required=True):
        self.source = source
        self.required = required

    def __call__(self, value):
        if not value and self.required is True:
            raise ValidationException(f"Field {self.source} is required")

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
            raise ValidationException(
                f"Field {self.source} should be a {self.target_type.__name__}, but it’s a {value.__class__}"
            )

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
