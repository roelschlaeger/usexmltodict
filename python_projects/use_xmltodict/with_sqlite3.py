# vim:ts=4:sw=4:tw=0:wm=0:et

from collections import OrderedDict
from sqlite3 import connect, OperationalError

FILENAME = "output_file.db"

########################################################################


def _build_keytypes(row):
    """Build a table of key types: assume TEXT except for a few exceptions"""
    keys = row.keys()
    keytypes = OrderedDict([(key, "TEXT") for key in keys])

    for c in ["@lat", "@lon"]:
        keytypes[c] = "REAL"

    for c in [
        "gsak:UserSort", "groundspeak:difficulty", "groundspeak:terrain"
    ]:
        keytypes[c] = "INTEGER"

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
    with connect(filename) as conn:
        c = conn.cursor()
        try:
            c.execute("DROP TABLE `waypoints`")
        except OperationalError:
            pass

########################################################################


def create_temp_db(filename, row):
    """Create a database from (name, type) information where names come from
`row`."""
    row_description = _build_row_description(row)
    with connect(filename) as conn:
        c = conn.cursor()
        cmd = "CREATE TABLE `waypoints` (%s)" % row_description
        c.execute(cmd)

########################################################################


def fill_temp_db(filename, row):
    with connect(filename) as conn:
        c = conn.cursor()
        row_keys = ", ".join(
            map(
                lambda x: "`%s`" % x,
                _build_keytypes(row).keys()
            )
        )
        qs = ", ".join(["?"] * len(row))
        cmd = "INSERT INTO `waypoints` (%s) VALUES (%s)" % (row_keys, qs)
        values_tuple = tuple(row.values())
        c.execute(cmd, values_tuple)


########################################################################


def get_data(filename=FILENAME):
    with connect(filename) as conn:
        c = conn.cursor()
        c.execute(
            "select `@lat`, `@lon`, text, sym, name, `gsak:UserSort`"
            " from `waypoints`"
        )
        data = c.fetchall()
        c.close()
    return data

########################################################################

# end of file
