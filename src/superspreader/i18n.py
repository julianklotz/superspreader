from .exceptions import TranslationMissing
from .messages import messages


def translate(key, locale="en", params={}):
    try:
        translation_string, comment = messages[locale][key]
    except KeyError as error:
        raise TranslationMissing(msg=str(error))

    return translation_string % params
