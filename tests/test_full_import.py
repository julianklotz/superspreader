# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import datetime
import unittest

from superspreader import BaseSheet, fields


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

    def setUp(self) -> None:
        self.sheet = AlbumSheet(path="./spreadsheets/albums.xlsx")

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
