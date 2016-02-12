#! C:\Users\Robert Oelschlaeger\AppData\Local\Programs\Python\Python35\python35.EXE

from sqlite3 import connect
from pprint import pprint

dbname = './Default/sqlite.db3'
print("Opening %s" % dbname)

c = connect(dbname)

with connect(dbname) as c:

    print("Selecting Code from Caches")
    c2 = c.execute('SELECT Code from Caches')

    all = c2.fetchall()

    non = [x[0] for x in all if x[0][:2] != u'GC']
    print(len(non), "non-cache waypoints")

    gc = [x[0] for x in all if x[0][:2] == u'GC']
    print(len(gc), "cache waypoints")

    result = {}
    for n in non:
        trait = n[2:]
        if 2 <= len(trait) <= 5:
            gcname = u"GC" + trait
            if not gcname in gc:
                if trait not in result:
                    result[trait] = []
                result[trait].append(n)

    print(len(result), "waypoints without a parent")
    pprint(result)

# end of file
