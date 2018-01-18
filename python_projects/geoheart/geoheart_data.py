#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 15 Feb 2017 08:55:30 AM CST
# Last Modified: Wed 15 Feb 2017 11:40:10 AM CST

# search strings
TEXT1 = "<p>(Rosetta) suggests that you will find the final at these coordinates:.. (.*), (.*)</p>"
TEXT2 = "<p>(Maurelle) thinks you should look for the final at these coordinates:.. (.*), (.*)</p>"

# file information
DATA = """
GC6ZJZ4	Geo(he)Art 1	http://www.geocaching.com/seek/cache_details.aspx?guid=be8fe001-7b7a-4aea-9c0a-624e8d0716b1
GC6ZJZ5	Geo(he)Art 2	http://www.geocaching.com/seek/cache_details.aspx?guid=8abddd5b-a7f8-4e76-a0a4-5c75a41274c0
GC6ZJZ7	Geo(he)Art 3	http://www.geocaching.com/seek/cache_details.aspx?guid=54e123b4-eb09-40e5-afd8-7f5d9e1de77e
GC6ZJZ8	Geo(he)Art 4	http://www.geocaching.com/seek/cache_details.aspx?guid=c9297972-4507-4ac3-a86d-01c684b02b2a
GC6ZJZ9	Geo(he)Art 5	http://www.geocaching.com/seek/cache_details.aspx?guid=082f9861-144f-4c47-8063-27601c5c10d0
GC6ZJZA	Geo(he)Art 6	http://www.geocaching.com/seek/cache_details.aspx?guid=e564e773-60b9-48c9-9a8d-8c28548a294c
GC6ZJZB	Geo(he)Art 7	http://www.geocaching.com/seek/cache_details.aspx?guid=f291162b-84a0-4c4a-920b-3e6b5c46313d
GC6ZJZC	Geo(he)Art 8	http://www.geocaching.com/seek/cache_details.aspx?guid=1cdcd3a8-070e-4a39-941d-5e4df4d4e3ea
GC6ZJZE	Geo(he)Art 9	http://www.geocaching.com/seek/cache_details.aspx?guid=0dbce577-079c-481f-9741-6d620b9000dd
GC6ZJZF	Geo(he)Art 10	http://www.geocaching.com/seek/cache_details.aspx?guid=f1e9f910-59a2-42b2-a12b-7860d4f7087b
GC6ZJZG	Geo(he)Art 11	http://www.geocaching.com/seek/cache_details.aspx?guid=7ab53b18-34a4-4700-8223-c94ba9b8970b
GC6ZJZH	Geo(he)Art 12	http://www.geocaching.com/seek/cache_details.aspx?guid=db22df3e-eb39-4cf4-890d-25585c5d27e5
GC6ZJZJ	Geo(he)Art 13	http://www.geocaching.com/seek/cache_details.aspx?guid=cc758f98-fc42-4a44-9aad-734338ac595f
GC6ZJZK	Geo(he)Art 14	http://www.geocaching.com/seek/cache_details.aspx?guid=c84081da-048a-463f-bd60-446d5111a131
GC6ZJZM	Geo(he)Art 15	http://www.geocaching.com/seek/cache_details.aspx?guid=5e2384dc-96ba-4dba-9eac-9ada39bdbaa1
GC6ZJZN	Geo(he)Art 16	http://www.geocaching.com/seek/cache_details.aspx?guid=94cb3dac-4342-4656-af7f-dd6d9e53a81b
GC6ZJZP	Geo(he)Art 17	http://www.geocaching.com/seek/cache_details.aspx?guid=411c2555-c194-4a9a-a343-7f13c9bed3e4
GC6ZJZQ	Geo(he)Art 18	http://www.geocaching.com/seek/cache_details.aspx?guid=0d0d1660-19f6-42be-929a-d0c9f9d28c9c
GC6ZJZR	Geo(he)Art 19	http://www.geocaching.com/seek/cache_details.aspx?guid=8d64eef0-fac0-4715-ae19-08eb0cbfc236
GC6ZJZT	Geo(he)Art 20	http://www.geocaching.com/seek/cache_details.aspx?guid=3434e827-2ee3-4e2a-9af7-3139956455b9
GC6ZJZV	Geo(he)Art 21	http://www.geocaching.com/seek/cache_details.aspx?guid=d59e6680-ee88-48cb-8980-d1b222df258f
GC6ZJZW	Geo(he)Art 22	http://www.geocaching.com/seek/cache_details.aspx?guid=04802374-fd6c-4772-a6cd-7bfc80c47849
"""

data = list((x.split("\t") for x in DATA.split("\n")[1:-1]))

# end of file
