import logging

EN = "en"
DE = "de"

SUPPORTED_LANGUAGES = (
    EN,
    DE,
)


def default_language():
    return SUPPORTED_LANGUAGES[0]


def translate(key, language=default_language(), params={}):
    from .messages import messages

    default_lang = default_language()
    if language not in SUPPORTED_LANGUAGES:
        logging.getLogger(__name__).info(
            f"Language {language} isn’t supported. Using {default_lang}"
        )
        language = default_lang

    try:
        translation_string, comment = messages[language][key]
    except KeyError:
        logging.getLogger(__name__).info(
            f"Language is supported, but translation not found."
            f"Falling back to {default_lang}"
        )
        translation_string, comment = messages[default_lang][key]

    return translation_string % params
