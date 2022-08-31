# Superspreader 🦠

Superspreader is a little helper library that simplifies working with spreadsheets.
It is built on top of [openpyxl](https://openpyxl.readthedocs.io/en/stable/).
OpenPyXL is its only dependency.

Instead of looping over rows and columns manually, the structure of a spreadsheet 
is described in a class:

```
from superspreader import fields
from superspreader.sheets import BaseSheet


class AlbumSheet(BaseSheet):
    """
    This class describes a sheet in an Excel document
    """
    
    sheet_name = "Albums" # The sheet is named “albums”
    header_rows = 3 # The sheet has three header rows
    
    # The column labels are in the second row.
    # It is *not* zero based to match the Excel row number
    label_row = 2
    

    # The columns
    artist = fields.CharField(source="Artist", required=True)
    album = fields.CharField(source="Album")
    release_date = fields.DateField(source="Release Date")
    average_review = fields.FloatField(source="Average Review")
    chart_position = fields.IntegerField(source="Chart Position")
```

Ready? Let’s load an Excel spreadsheet!

```
if __name__ == "__main__":
    sheet = AlbumSheet("albums.xlsx")
    # Load and parse data from the document
    sheet.load()
    
    print(sheet.has_errors)
    # False
    print(sheet.errors)
    # []
    print(sheet.infos)
    # []
    
    for row_dict in sheet:
        print(row_dict)
        
# {'artist': 'David Bowie', 'album': 'Toy', 'release_date': datetime.date(2022, 1, 7), 'average_review': 4.3, 'chart_position': 5}
# {'artist': 'The Wombats', 'album': 'Fix Yourself, Not The World', 'release_date': datetime.date(2022, 3, 7), 'average_review': 3.9, 'chart_position': 7}
# {'artist': 'Kokoroko', 'album': 'Could We Be More', 'release_date': datetime.date(2022, 8, 1), 'average_review': 4.7, 'chart_position': 30}   
```

In `tests/spreadsheets` is a sample spreadsheet that is used for testing. Feel free to fiddle around.

There’s a lot more to say and I’ll update the documentation as I go.

## Changelog

### 0.1.4

* Adds basic documentation on how to use superspreader

---
The API is inspired by [Django’s model API](https://docs.djangoproject.com/en/dev/ref/models/) and [ElasticSearch DSL](https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#document).


