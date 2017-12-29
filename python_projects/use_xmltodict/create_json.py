# create a JSON file from a .gpx file

import json
from xmltodict import parse


########################################################################

def create_outfile_json(doc, outfile):
    """Create a JSON file in outfile describing doc"""

    # create the JSON string
    s = json.dumps(doc, indent=1)

    # write it to a text file
    with open(OUTFILE, "w") as ofile:
        ofile.write(s)

    # show that processing is complete
    print(f"JSON written to {outfile}")


########################################################################

def main(filename, outfile):

    print(f"Reading from {filename}")
    jsontext = open(filename, "rb").read()
    doc = parse(jsontext)
    create_outfile_json(doc, outfile)


########################################################################

if __name__ == "__main__":

    FILENAME = "temp.gpx"
    OUTFILE = "outfile.json"

    main(FILENAME, OUTFILE)

# end of file
