# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import datetime
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

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
    Test the process of importing a spreadsheet
    """

    def _file_path(self, file_name):
        tests_dir = Path(__file__).parent.absolute()
        path = os.path.join(tests_dir, "spreadsheets", file_name)
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
        self.assertEqual("Row 6: Skipped row", self.sheet.infos[0])

    def test_errors(self):
        path = self._file_path("albums_with_errors.xlsx")
        sheet_with_errors = AlbumSheet(path)
        sheet_with_errors.load()

        self.assertTrue(sheet_with_errors.has_errors)
        self.assertEqual(sheet_with_errors.errors[0], "Row 7: “Album” is required")

    def test_empty_sheet_with_extra_data(self):
        """Tests whether empty rows are skipped, even when extra data is provided"""
        path = self._file_path("albums_empty.xlsx")
        sheet = AlbumSheet(path, extra_data={"status": "released"})
        self.assertFalse(sheet.has_errors)
        self.assertEqual(len(sheet), 0)

    def test_extra_data_static(self):
        """Tests whether extra data is returned in the resulting row"""
        fp = self._file_path("albums.xlsx")
        sheet = AlbumSheet(path=fp, extra_data={"status": "released"})
        sheet.load()
        self.assertEqual(sheet.rows()[0].get("status"), "released")

    def test_extra_data_dynamic(self):
        """Tests whether callables in extra data are called"""
        fp = self._file_path("albums.xlsx")
        test_fn = MagicMock()
        sheet = AlbumSheet(path=fp, extra_data={"test_fn": test_fn})
        sheet.load()
        test_fn.assert_called()

    def test_extra_data_dynamic_args(self):
        """Tests whether callables in extra data are called with the row"""
        fp = self._file_path("albums.xlsx")

        def test_fn(row):
            self.assertIsInstance(row, dict)

        sheet = AlbumSheet(path=fp, extra_data={"test_fn": test_fn})
        sheet.load()
