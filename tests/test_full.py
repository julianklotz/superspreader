# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from superspreader import BaseSheet, fields


class AlbumSheet(BaseSheet):
    sheet_name = "Albums"
    header_rows = 2

    artist = fields.CharField(source="Artist")
    album = fields.CharField(source="Album")
    # release_date = fields.DateField(source='Release Date')
    # average_review = fields.FloatField(source='Average Review')
    # chart_position = fields.IntegerField(source='Chart position')


class TestFull(unittest.TestCase):
    """
    Test the process of importing a whole spreadsheet
    """

    def test_all(self):
        sheet = AlbumSheet(path="./spreadsheets/albums.xlsx")
        sheet.load()

        for record in sheet:
            print(record.artist)

        print(sheet.errors)


if __name__ == "__main__":
    unittest.main()
