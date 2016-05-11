from xml.etree import ElementTree as ET

OUTNAME = "make_rte.xml"
TAG_BASE = "http://www.topografix.com/GPX/1/1/"

def make_tag(tag, tag_base=TAG_BASE):
    return "{%s}%s" % (tag_base, tag)

class make_rte(object):
    last_route = 0

    def __init__(self,
        name="",
        cmt="",
        desc="",
        src="",
        link=None,
        number=0,
        rtype="",
        extensions=[],
        rtept=[]
        ):
        self.name = name
        self.cmt = cmt
        self.desc = desc
        self.src = src
        self.link = link
        self.number = number
        self.rtype = rtype
        self.extensions = extensions
        self.rtept = rtept

    def to_xml(self):
        rte = ET.Element(make_tag("rte"))

        if self.name:
            name = ET.Element(make_tag("name"))
            name.text = self.name
            rte.append(name)

        if self.cmt:
            cmt = ET.Element(make_tag("cmt"))
            cmt.text = self.cmt
            rte.append(cmt)

        if self.desc:
            desc = ET.Element(make_tag("desc"))
            desc.text = self.desc
            rte.append(desc)

        if self.src:
            src = ET.Element(make_tag("src"))
            src.text = self.src
            rte.append(src)

        if self.link:
            link = ET.Element(make_tag("link"))
            link.text = self.link
            rte.append(link)

        if self.number:
            number = ET.Element(make_tag("number"))
            number.text = str(self.number)
            rte.append(number)

        if self.rtype:
            rtype = ET.Element(make_tag("type"))
            rtype.text = self.rtype
            rte.append(rtype)

        if self.extensions:
            extensions = ET.Element(make_tag("extensions"))
            extensions.text = self.extensions
            rte.append(extensions)

        if self.rtept:
            rtept = ET.Element(make_tag("rtept"))
            rtept.text = self.rtept
            rte.append(rtept)

        return rte

rte = make_rte(name="My Route", number=1).to_xml()

ET.register_namespace("", TAG_BASE)
ofile = ET.ElementTree(rte)
outfile = open(OUTNAME, "wb")
ofile.write(outfile, encoding="utf-8", xml_declaration=True, method="xml")
outfile.close()
print("output is in %s" % OUTNAME)
