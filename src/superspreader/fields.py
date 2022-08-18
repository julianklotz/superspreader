from abc import ABC

from .exceptions import ValidationException


class BaseField(ABC):
    def __init__(self, source, required=True):
        self.source = source
        self.required = required
        self.target = None

    def __call__(self, value):
        self.value = value

        if not self.value and self.required is True:
            raise ValidationException(f"Field {self.source} is required")

        return self.clean()

    def clean(self):
        raise NotImplementedError()


class CharField(BaseField):
    def clean(self):
        if self.value:
            return str(self.value)
