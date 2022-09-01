# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import datetime
import os
import unittest
from pathlib import Path

from superspreader import fields
from superspreader.sheets import BaseSheet


class AlbumSheet(BaseSheet):
    sheet_name = "Albums"
    header_rows = 3
    label_row = 2

    artist = fields.CharField(source="Artist")
    album = fields.CharField(source="Album")
    release_date = fields.DateField(source="Release Date")
    average_review = fields.FloatField(source="Average Review")
    chart_position = fields.IntegerField(source="Chart Position")


class TestFullImport(unittest.TestCase):
    """
    Test the process of importing a whole spreadsheet
    """

    def _file_path(self, file_name):
        script_dir = Path(__file__).parent.absolute()
        path = os.path.join(script_dir, "spreadsheets", file_name)
        return path

    def setUp(self) -> None:
        self.sheet = AlbumSheet(self._file_path("albums.xlsx"))

    def test_basics(self):
        self.sheet.load()
        self.assertFalse(self.sheet.has_errors)
        self.assertEqual(len(self.sheet), 3)

    def test_record(self):
        self.sheet.load()
        first_record = self.sheet[0]

        self.assertEqual(first_record.get("album"), "Toy")
        self.assertEqual(first_record.get("artist"), "David Bowie")
        self.assertEqual(first_record.get("release_date"), datetime.date(2022, 1, 7))
        self.assertEqual(first_record.get("average_review"), 4.3)
        self.assertEqual(first_record.get("chart_position"), 5)

    def test_rows(self):
        self.sheet.load()
        rows = self.sheet.rows(exclude=["album"])
        with self.assertRaises(KeyError):
            rows[0]["album"]

    def test_info(self):
        self.sheet.load()
        self.assertEqual("Sheet Albums, row 6: Skipped row", self.sheet.infos[0])

    def test_extra_data(self):
        extra = {"test": "1-2-3"}
        sheet = AlbumSheet(self._file_path("albums.xlsx"), extra_fields=extra)
        sheet.load()
        first_record = sheet[0]

        self.assertEqual(first_record.get("test"), "1-2-3")

    def test_errors(self):
        path = self._file_path("albums_with_errors.xlsx")
        sheet_with_errors = AlbumSheet(path)
        sheet_with_errors.load()

        self.assertTrue(sheet_with_errors.has_errors)
        self.assertEqual(
            sheet_with_errors.errors[0], "Sheet Albums, row 7: Field Album is required"
        )
