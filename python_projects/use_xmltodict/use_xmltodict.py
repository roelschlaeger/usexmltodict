from xmltodict import parse
import json

FILENAME = "temp.gpx"
JSONFILE = "outfile.json"
TEXTFILE = "outfile.txt"

with open(TEXTFILE, "w") as outfile:

    doc = parse(open(FILENAME, "rb").read())

    s = json.dumps(doc, indent=1)
    with open("outfile.json", "w") as ofile:
        ofile.write(s)
    print("JSON written to %s" % JSONFILE)

    wpts = doc['gpx']["wpt"]
    w0 = wpts[0]

    def show(s):
        for k in s.keys():
            print(bytes(k, 'utf8'), file=outfile, end=" ")
            sk = str(s[k])[:80]
            print(sk, file=outfile)

    show(w0)

    gpx = doc['gpx']
    show(gpx)

    wpt = gpx['wpt']
    for w in wpt:
        print(file=outfile)
        show(w)

print("Output is in %s" % TEXTFILE)

# end of file
