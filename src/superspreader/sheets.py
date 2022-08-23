from abc import ABC

from openpyxl import load_workbook

from .exceptions import ImproperlyConfigured, ValidationException
from .fields import BaseField
from .i18n import translate as _


class BaseSheet(ABC):
    header_rows = 1
    sheet_name = None
    label_row = None

    def __init__(self, path, locale="en"):
        self.locale = locale
        self.path = path
        self._fields = self._build_fields()
        self._rows = []
        self._infos = []
        self._errors = []

        self._check()

    def shall_skip(self, row: dict):
        """
        Indicates whether to skip a row. It return True (i.e. skip) if there’s
        at least one truthy field.
        :param row: A dictionary representing a row
        :return: boolean, skip or not
        """
        values = row.values()
        # When there’s at least one truthy value, don’t skip.
        if any(values):
            return False
        return True

    def load(self):
        """
        Loads the spreadsheet and map its contents to dicts.
        :return:
        """
        header_rows = self.get_header_rows()
        fields = self._fields
        sheet = self.__get_sheet()

        if self.has_errors:
            return

        column_map = self.__column_map(sheet)
        self.__check_columns_present(column_map)

        if self.has_errors:
            return

        min_row = header_rows + 1

        for row_index, row_cells in enumerate(sheet.iter_rows(min_row=min_row)):
            row_dict = {}
            error_cache = []
            for name, field in fields.items():
                cell_index = column_map.get(field.source)

                try:
                    cell = row_cells[cell_index]
                    try:
                        row_dict[name] = field(cell.value, self.locale)
                    except ValidationException as error:
                        row_dict[name] = None
                        error_cache.append((str(error), row_index + header_rows))
                except KeyError:
                    pass

            if self.shall_skip(row_dict):

                self._add_info("Skipped row", index=row_index + header_rows)
                continue
            else:
                self._rows.append(row_dict)
                self._add_errors(error_cache)

    def get_sheet_name(self):
        """
        Gets the sheet
        :return: str
        """
        return self.sheet_name

    def get_header_rows(self):
        """
        Gets the number of header rows
        :return: int
        """
        return self.header_rows

    def get_label_row(self):
        """
        Gets the index of the row that contains column labels
        :return: int
        """
        if self.label_row:
            return self.label_row
        return self.get_header_rows() - 1

    @property
    def errors(self):
        return self._errors

    @property
    def has_errors(self):
        return len(self._errors) > 0

    @property
    def infos(self):
        return self._infos

    @property
    def has_infos(self):
        return len(self._infos) > 0

    def __getitem__(self, item):
        if item < 0 or (item > len(self) - 1):
            raise IndexError()

        return self._rows[item]

    def __len__(self):
        return len(self._rows)

    #
    # === Protected ===
    #

    def _build_fields(self) -> dict:
        fields = {}
        for attr, field in self.__class__.__dict__.items():
            if isinstance(field, BaseField):
                fields[attr] = field

        return fields

    def _add_error(self, message, index=None) -> None:
        # Add to row index, if it’s related to a row.
        if isinstance(index, int):
            message = _(
                "sheet.row_info",
                self.locale,
                params={"row": index + 2, "message": message},
            )
        self._errors.append(message)

    def _add_errors(self, errors) -> None:
        for error in errors:
            if isinstance(error, tuple):
                error_len = len(error)
                if error_len == 2:
                    self._add_error(error[0], error[1])
                elif error_len == 1:
                    self._add_error(error[0])
                else:
                    raise ValueError("Error tuple too long.")
            else:
                self._add_error(error)

    def _add_info(self, message, index=None) -> None:
        # Add to row index, if it’s related to a row.
        if isinstance(index, int):
            message = _(
                "sheet.row_info",
                self.locale,
                params={"row": index + 2, "message": message},
            )
        self._infos.append(message)

    def _check(self) -> None:
        """
        Perform configuration checks. Add your own in subclasses
        :raises ImproperlyConfigured
        """
        if self.get_header_rows() < 1:
            raise ImproperlyConfigured("Sheets must have at least one header row")

        if not self.sheet_name:
            raise ImproperlyConfigured("No sheet name set")

    #
    # === Private ===
    #

    def __column_map(self, sheet) -> dict:
        """
        Takes a sheet and returns a dictionary, that maps column names to column indexes.

        Example:
        ```
        {
            "Artist": 0,
            "Album": 1,
            "Release Date": 2
        }
        ```

        :param sheet: Worksheet from openpyxl
        :return: A dictionary that maps column names to indexes
        """
        column_map = {}
        label_row = self.get_label_row()

        for index, column in enumerate(
            sheet.iter_cols(0, sheet.max_column, min_row=label_row, max_row=label_row)
        ):
            column_map[column[0].value] = index

        return column_map

    def __check_columns_present(self, column_map) -> None:
        """
        Checks whether the columns (described by the source attribute of fields) are present.
        Missing columns are added to error list.

        :param column_map: The column map
        """
        fields = self._build_fields()
        used_fields = set([field.source for field in fields.values()])
        all_fields = set(column_map.keys())

        for field in used_fields:
            if field not in all_fields:
                msg = _("sheet.column_missing", self.locale, params={"column": field})
                self._add_error(msg)

    def __get_sheet(self):
        wb = load_workbook(filename=self.path, data_only=True)
        sheet_name = self.get_sheet_name()

        try:
            return wb[sheet_name]
        except KeyError:
            msg = _("sheet.sheet_missing", self.locale, params={"sheet": sheet_name})
            self._add_error(msg)
