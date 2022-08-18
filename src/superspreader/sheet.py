import os
from abc import ABC

from .exceptions import ImproperlyConfigured


class BaseSheet(ABC):
    header_rows = 1
    sheet_name = None

    def __init__(self, path=None, file=None):
        self.path = path
        self.file = file

        self.check()

    def check(self):
        if self.get_header_rows() < 1:
            raise ImproperlyConfigured("Sheets must have at least one header row")

        if self.path is None and self.file is None:
            raise ImproperlyConfigured("Either path or file has to be passed")

        if not self.sheet_name:
            raise ImproperlyConfigured("No sheet name set")

    def get_sheet_name(self):
        return self.sheet_name

    def get_header_rows(self):
        return self.header_rows

    def get_file(self):
        if not self.file:
            if os.path.exists(self.path):
                self.file = open(self.path, "r")
            else:
                raise ValueError("%s is not a file" % self.path)
        return self.file

    def __enter__(self):
        if not self.file:
            self.get_file()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
