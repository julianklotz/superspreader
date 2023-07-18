# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import os
import unittest
from pathlib import Path

from superspreader import fields
from superspreader.exceptions import ImproperlyConfigured
from superspreader.sheets import BaseSheet


def file_path(file_name):
    tests_dir = Path(__file__).parent.absolute()
    path = os.path.join(tests_dir, "spreadsheets", file_name)
    return path


class ContactSheet(BaseSheet):
    sheet_name = "Contacts"

    id = fields.CharField(source="ID", unique=True)
    name = fields.CharField(source="Name")


class SheetTestCase(unittest.TestCase):
    def test_sheet_name(self):
        class AlbumSheet(BaseSheet):
            pass

        with self.assertRaises(ImproperlyConfigured):
            AlbumSheet(path="test")

    def test_path_or_file(self):
        class AlbumSheet(BaseSheet):
            pass

        with self.assertRaises(ImproperlyConfigured):
            AlbumSheet(path="test")

    def test_no_header_rows(self):
        class AlbumSheet(BaseSheet):
            header_rows = 0

        with self.assertRaises(ImproperlyConfigured):
            AlbumSheet(path="test")

    def test_attributes_are_inherited(self):
        class ASheet(BaseSheet):
            sheet_name = "A Sheet"
            a_field = fields.CharField(source="")

        class BSheet(ASheet):
            pass

        sheet = BSheet(path="test")
        sheet_fields = sheet._build_fields()

        self.assertTrue("a_field" in sheet_fields)

    def test_unique_violation(self):
        """
        Tests whether unique fields are validate properly
        """
        path = file_path("contacts_duplicates.xlsx")
        sheet = ContactSheet(path)
        sheet.load()

        self.assertEqual(len(sheet.errors), 1)
        self.assertEqual(
            sheet.errors[0],
            "“ID” must contain unique values only, but “1” occurs 1 times",
        )
