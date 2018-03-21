# vim:ts=4:sw=4:tw=0:wm=0:et

"""
doc string
"""


# file:///C:/Users/Robert%20Oelschlaeger/Downloads/python-excel.pdf

from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
from xlrd import cellname

FILENAME = "default.xls"
# FILENAME = "simple.xls"

print(open_workbook(FILENAME))

with open(FILENAME, 'rb') as f:
    print(
        open_workbook(
            file_contents=mmap(
                f.fileno(),
                0,
                access=ACCESS_READ
            )
        )
    )

A_STRING = open(FILENAME, 'rb').read()
print(open_workbook(file_contents=A_STRING))

########################################################################

# from xlrd import open_workbook
WORKBOOK = open_workbook(FILENAME)
for s in WORKBOOK.sheets():
    print('Sheet:', s.name)
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            values.append(s.cell(row, col).value)
            print(','.join(values))
    print()


########################################################################

BOOK = open_workbook(FILENAME)
SHEET = BOOK.sheet_by_index(0)
print("sheet.name=", SHEET.name)
print("sheet.nrows=", SHEET.nrows)
print("sheet.ncols=", SHEET.ncols)
for row_index in range(SHEET.nrows):
    for col_index in range(SHEET.ncols):
        print(cellname(row_index, col_index), '-', end=" ")
        print(SHEET.cell(row_index, col_index).value)

########################################################################
