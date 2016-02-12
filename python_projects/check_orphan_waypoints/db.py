from sqlite3 import *
dir()
help(connect)
connect('Kansas/sqlite.db3')
c = connect('Kansas/sqlite.db3')
c
dir(c)
help(c.cursor)
cur = c.cursor()
dir(cur)
cur.fetchone()
a  = cur.fetchone()
a
a  = cur.fetchall(I)
a  = cur.fetchall()
a
help fetchall
help(fetchall)
help(cur.fetchall)
help(cur)
cur.execute('SELECT Code from Caches')
c2 = cur.execute('SELECT Code from Caches')
dir(c2)
len(c2)
c2.fetchall()
all=c2.fetchall()
all
c2 = cur.execute('SELECT Code from Caches')
all=c2.fetchall()
all
non = [x for x in all if x[:2] != 'GC']
non
non = [x for x in all if x[:2] != u'GC']
non
x=all[0]
x
non = [x for x in all if x[0][:2] != u'GC']
non
non = [x[0] for x in all if x[0][:2] != u'GC']
non
gc = [x[0] for x in all if x[0][:2] == u'GC']
gc
for n in non:
    gcname = u"GC" + non[2:]
    if not gcname in gc:
        print(non, gcname)
    gcname = u"GC" + unicode(non[2:])
gcname
for n in non:
    gcname = u"GC" + unicode(non[2:])
    if not gcname in gc:
        print(non, gcname)
non
for n in non:
    gcname = u"GC" + n[2:]
    if not gcname in gc:
        print(non, gcname)
for n in non:
    gcname = u"GC" + n[2:]
    if not gcname in gc:
        print(n, gcname)
%hist?
%history?
%history -f db.py
