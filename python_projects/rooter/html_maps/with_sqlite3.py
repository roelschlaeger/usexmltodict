#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et

"""Build a table of key types: assume TEXT except for a few exceptions"""

from collections import OrderedDict
from sqlite3 import connect, OperationalError

FILENAME = "output_file.db"

########################################################################


def _build_keytypes(row):
    """Build a table of key types: assume TEXT except for a few exceptions"""
    keys = row.keys()
    keytypes = OrderedDict([(key, "TEXT") for key in keys])

    for col in ["@lat", "@lon"]:
        keytypes[col] = "REAL"

    for col in [
            "gsak:UserSort",
            "groundspeak:difficulty",
            "groundspeak:terrain"
        ]:
        keytypes[col] = "INTEGER"

    return keytypes

########################################################################


def _build_row_description(row):
    keytypes = _build_keytypes(row)
    result = ", ".join(
        ["`%s` %s" % (key, value) for key, value in keytypes.items()]
    )

    return result

########################################################################


def delete_temp_db(filename):
    """Delete "waypoints" table from database 'filename'

    Arguments:
        filename {str} -- database filename
    """
    with connect(filename) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE `waypoints`")
        except OperationalError:
            pass

########################################################################


def create_temp_db(filename, row):
    """Create a database from (name, type) information where names come from
`row`."""
    row_description = _build_row_description(row)
    with connect(filename) as conn:
        cursor = conn.cursor()
        cmd = "CREATE TABLE `waypoints` (%s)" % row_description
        cursor.execute(cmd)

########################################################################


def fill_temp_db(filename, row):
    """File temporary database 'filename' with data from 'row'"""
    with connect(filename) as conn:
        cursor = conn.cursor()
        row_keys = ", ".join(
            map(
                lambda x: "`%s`" % x,
                _build_keytypes(row).keys()
            )
        )
        questions = ", ".join(["?"] * len(row))
        cmd = "INSERT INTO `waypoints` (%s) VALUES (%s)" % (row_keys, questions)
        values_tuple = tuple(row.values())
        cursor.execute(cmd, values_tuple)


########################################################################


def get_data(filename=FILENAME):
    """Fetch all data from 'filename' database"""
    with connect(filename) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select `@lat`, `@lon`, text, sym, name, `gsak:UserSort`, `@href`"
            " from `waypoints`"
        )
        data = cursor.fetchall()
        cursor.close()
    return data

########################################################################

# end of file
