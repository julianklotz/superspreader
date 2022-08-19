# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from superspreader import BaseSheet
from superspreader.exceptions import ImproperlyConfigured


class TestSheet(unittest.TestCase):
    def test_sheet_name(self):
        class AlbumSheet(BaseSheet):
            pass

        with self.assertRaises(ImproperlyConfigured) as error:
            AlbumSheet(path="test")

    def test_path_or_file(self):
        class AlbumSheet(BaseSheet):
            pass

        with self.assertRaises(ImproperlyConfigured) as error:
            AlbumSheet(path="test")

    def test_no_header_rows(self):
        class AlbumSheet(BaseSheet):
            header_rows = 0

        with self.assertRaises(ImproperlyConfigured) as error:
            AlbumSheet(path="test")
