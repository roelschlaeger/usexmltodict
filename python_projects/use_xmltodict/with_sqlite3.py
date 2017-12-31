# vim:ts=4:sw=4:tw=0:wm=0:et

from collections import OrderedDict
from sqlite3 import connect, OperationalError


def build_row_description(row):
    keys = row.keys()
    keytypes = OrderedDict([(key, "TEXT") for key in keys])

    for c in ["@lat", "@lon"]:
        keytypes[c] = "REAL"

    for c in [
        "gsak:UserSort", "groundspeak:difficulty", "groundspeak:terrain"
    ]:
        keytypes[c] = "INTEGER"

    result = ", ".join(
        ["`%s` %s" % (key, value) for key, value in keytypes.items()]
    )

    return result


def create_temp_db(filename, row):
    with connect(filename) as conn:
        c = conn.cursor()
        row_description = build_row_description(row)
        try:
            c.execute("DROP TABLE `waypoints`")
        except OperationalError:
            pass
        qs = ", ".join(["?"] * len(row))
        cmd = "CREATE TABLE `waypoints` (%s)" % qs
        print(cmd, "\n", row_description, "\n")
        c.execute(cmd, (row_description,))

# end of file
