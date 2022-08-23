from .i18n import DE, EN

messages = {
    EN: {
        "field.wrong_type": (
            "Field %(field)s should be of type %(target_type)s, but it’s of type %(actual_type)s",
            None,
        ),
        "field.is_required": ("Field %(field)s is required", None),
        "field.timecode_parse_error": (
            "Field %(field)s has an invalid format: %(_timecode)s",
            None,
        ),
        "field.related_does_not_exist": (
            "Related object identified by %(value)s on field %(field)s does not exist",
            None,
        ),
        "field.related_multiple_objects_returned": (
            "More than one related object identified by %(value)s on field %(field)s",
            None,
        ),
        "sheet.row_info": ("Row %(row)s: %(message)s", None),
        "sheet.column_missing": ("Column %(column)s not present in sheet", None),
        "sheet.sheet_missing": ("Sheet %(sheet)s not present in document", None),
    },
    DE: {
        "field.wrong_type": (
            "Das Feld %(field)s sollte den Typ %(target_type)s haben, aber der"
            "Typ ist %(actual_type)s",
            None,
        ),
        "field.is_required": ("Das Feld %(field)s muss ausgefüllt sein", None),
        "field.timecode_parse_error": (
            "Das Feld %(field)s hat ein ungültiges Format: %(_timecode)s",
            None,
        ),
        "field.related_does_not_exist": (
            "Ein Objekt mit %(value)s beim Feld %(field)s existiert nicht",
            None,
        ),
        "field.related_multiple_objects_returned": (
            "Mehr als ein Objekt mit %(value)s beim Feld %(field)s gefunden",
            None,
        ),
        "sheet.row_info": ("Zeile %(row)s: %(message)s", None),
        "sheet.column_missing": ("Die Spalte %(column)s fehlt im Blatt", None),
        "sheet.sheet_missing": ("Das Blatt %(sheet)s ist nicht vorhanden", None),
    },
}
