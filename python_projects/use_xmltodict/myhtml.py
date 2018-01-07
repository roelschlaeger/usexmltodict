# vim:ts=4:sw=4:tw=0:wm=0:et:noic

"""Import non-standard html.py"""

from os.path import abspath
import sys

p = abspath('.') + "/html-1.16"
sys.path.insert(1, p)
from html import *

if __name__ == "__main__":

    doc = HTML()
    doc.title("This is the title")

    head = doc.head(meta='charset="utf-8"')
    body = doc.body()

    d1 = body.div()
    t = d1.table(border="1px solid black", border_collapse="collapse", cellpadding="3")
    thead = t.thead()
    tr = thead.tr
    tr.th("Index")
    tr.th("Link")
    tbody = t.tbody()
    for i in range(10):
        tr = tbody.tr()
        tr.td(str(i), align="center")
        tr.td.a("Link %s" % i, href="http://example.com/location_%s" % i, align="center")
    print(doc)

    # end of file
