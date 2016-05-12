# -*- encoding="utf-8" -*-
########################################################################

from __future__ import print_function

########################################################################

GPX_NAMESPACE = "http://www.topografix.com/GPX/1/1"
GSAK_NAMESPACE = "http://www.gsak.net/xmlv1/6"
GROUNDSPEAK_NAMESPACE = "http://www.groundspeak.com/cache/1/0/1"

ITEM_TEXT = "MAKE_RTEPT_WAYPOINT"

from xml.etree import ElementTree as ET
ET.register_namespace("", GPX_NAMESPACE)
ET.register_namespace("GSAK", GSAK_NAMESPACE)
ET.register_namespace("groundspeak", GROUNDSPEAK_NAMESPACE)

def get_usersort(w0):
    try:
        value = w0\
.find(make_tag("extensions"))\
.find(make_tag("wptExtension", GSAK_NAMESPACE))\
.find(make_tag("UserSort", GSAK_NAMESPACE))\
.text
        # print("Success: %s" % value, list(w0))
    except AttributeError as error:
        value = ""

    return value

########################################################################


class DummyText(object):
    text = ""

    def __init__(self, item):
        if item is None:
            self.text = ""
        elif type(item) == type(""):
            self.text = item
        else:
            self.text = item.text

########################################################################


def make_tag(s, ns=GPX_NAMESPACE):
    return "{%s}%s" % (ns, s)

ele_tag = make_tag("ele")
time_tag = make_tag("time")
magvar_tag = make_tag("magvar")
geoidheight_tag = make_tag("geoidheight")
name_tag = make_tag("name")
cmt_tag = make_tag("cmt")
desc_tag = make_tag("desc")
src_tag = make_tag("src")
link_tag = make_tag("link")
sym_tag = make_tag("sym")
rtype_tag = make_tag("type")
fix_tag = make_tag("fix")
sat_tag = make_tag("sat")
hdop_tag = make_tag("hdop")
vdop_tag = make_tag("vdop")
pdop_tag = make_tag("pdop")
ageofdgpsdata_tag = make_tag("ageofdgpsdata")
dgpsid_tag = make_tag("dgpsid")
extensions_tag = make_tag("extensions")

usersort_tag = make_tag("UserSort", GSAK_NAMESPACE)
# print(usersort_tag)

rtept_tag = make_tag("rtept")

########################################################################


def add_rtepts_from_wpts(rte, wpts):

    # create a list for temporarily storing accumulating rtepts
    rtept_list = []

    # add modified wpts to rte as they are seen
    for wpt in wpts:

        # get location from attributes
        lat = wpt.attrib["lat"]
        lon = wpt.attrib["lon"]

        # make a new <wpt> element from the old one
        new_wpt = ET.Element(wpt_tag, {"lat": lat, "lon": lon})

        # make an <rtept> element
        rtept = ET.Element(rtept_tag, {"lat": lat, "lon": lon})

        # gather this information first
        _name = DummyText(wpt.find(name_tag))
        _desc = DummyText(wpt.find(desc_tag))
        _usersort = DummyText(get_usersort(wpt))

        def _fabricated_name():
            if _usersort:
                return "%s %s %s " % (_usersort.text, _desc.text, _name.text)
            return "%s %s" (_desc.text, _name.text)

        # pass along most of the information to the new_wtp (but not
        # extensions)
        for tag in [
            ele_tag,                           # KEEP THESE IN THIS ORDER #
            time_tag,                          #
            magvar_tag,                        #
            geoidheight_tag,                   #
            name_tag,                          #
            cmt_tag,                           #
            desc_tag,                          #
            src_tag,                           #
            link_tag,                          #
            sym_tag,                           #
            rtype_tag,                         #
            fix_tag,                           #
            sat_tag,                           #
            hdop_tag,                          #
            vdop_tag,                          #
            pdop_tag,                          #
            ageofdgpsdata_tag,                 #
            dgpsid_tag,                        # KEEP THESE IN THIS ORDER #
            # extensions_tag                   # not passing along extensions
        ]:

            # check for the presence of the tag in the old wpt
            found = wpt.find(tag)

            # if it is there, add it to the <rtept> and new <wpt>, removing the
            # tail information
            if found is not None:

                item2 = ET.SubElement(new_wpt, tag)
                item2.text = found.text

                # interchange the <name> and <desc> tags
                if tag == name_tag:
                    item = ET.SubElement(rtept, tag)
                    # item.text = "%s %s" % (_usersort.text, _desc.text)
                    item.text = _fabricated_name()
                elif tag == desc_tag:
                    item = ET.SubElement(rtept, tag)
                    item.text = _name.text
                else:
                    item = ET.SubElement(rtept, tag)
                    item.text = found.text

        rtept_list.append(rtept)
        rte.append(new_wpt)

    # now transfer all of the collected <rtept> data
    for rtept in rtept_list:
        rte.append(rtept)

#######################################################################

if __name__ == "__main__":

    from gpx2kml import pretty_print

    # not needed elsewhere
    wpt_tag = make_tag("wpt")

    # get wpts elements from an existing file
    root = ET.parse("topo840b - collinsville IL.gpx").getroot()
    wpts = root.findall(wpt_tag)

    # build an output gpx file
    gpx = ET.Element("gpx")

    # add all current wpts as-is
    for wpt in wpts:
        for item in wpt.iter():
            item.tail = ""
            txt = item.text
            # print("'%s'" % txt)
            if txt is not None and txt.strip() == "":
                item.text = ""
            if item.tag == rtype_tag:
                item.text = "%s %s" % (ITEM_TEXT, item.text)
        gpx.append(wpt)

    # with a rte
    rte = ET.SubElement(gpx, "rte")

    # add the wpts to the rte as rtepts
    add_rtepts_from_wpts(rte, wpts)

    OUTNAME = "_make_rtept.gpx"
    ofile = open(OUTNAME, "wb")
    pretty_print(ofile, gpx, indent=" ")
    ofile.close()

    print("Output is in %s" % OUTNAME)
