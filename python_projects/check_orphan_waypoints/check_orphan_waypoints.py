#! C:/Users/"Robert Oelschlaeger"/AppData/Local/Programs/Python/Python35/python35.EXE

from xml.etree import ElementTree as ET
from pprint import pprint

fname = 'code_name.gpx'

tree = ET.parse(fname)

root = tree.getroot()
# print(root.tag)

wpt_tag = root.tag.replace('gpx', 'wpt')
# print(wpt_tag)

wpts = root.findall(wpt_tag)
print(len(wpts), "waypoints")

names = [wpt[1].text for wpt in wpts]

non = [n for n in names if n[0:2] != "GC"]
print(len(non), "non-GC names")

gc = [n for n in names if n[0:2] == "GC"]
print(len(gc), "GC names")


def check():
    result = []
    for name in non:
        if 4 <= len(name) <= 7:
            gcname = "GC" + name[2:]
            if gcname not in gc:
                print(gcname, name)
                result.append(name)
        else:
            print(name, "needs separate checking?")
    return result

result = check()
print(len(result), "items in result")
print()
pprint(result)
print()

# end of file
