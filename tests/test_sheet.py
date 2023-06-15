# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from superspreader import fields
from superspreader.exceptions import ImproperlyConfigured
from superspreader.sheets import BaseSheet


class TestSheet(unittest.TestCase):
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
