class BaseException(Exception):
    def __init__(self, msg: str, hint=None):
        self.msg = msg
        self.hint = hint

    def __str__(self):
        if self.msg and self.hint:
            return f"{self.msg}\n{self.hint}"

        return self.msg


class ImproperlyConfigured(BaseException):
    pass


class ValidationException(BaseException):
    pass


class TranslationMissing(BaseException):
    pass
