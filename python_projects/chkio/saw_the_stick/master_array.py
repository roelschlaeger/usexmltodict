# vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

from __future__ import print_function

master_array = {
    4: [1, 3],
    9: [3, 6],
    10: [1, 3, 6],
    16: [6, 10],
    19: [3, 6, 10],
    20: [1, 3, 6, 10],
    25: [10, 15],
    31: [6, 10, 15],
    34: [3, 6, 10, 15],
    35: [1, 3, 6, 10, 15],
    36: [15, 21],
    46: [10, 15, 21],
    49: [21, 28],
    52: [6, 10, 15, 21],
    55: [3, 6, 10, 15, 21],
    56: [1, 3, 6, 10, 15, 21],
    64: [15, 21, 28],
    74: [10, 15, 21, 28],
    80: [6, 10, 15, 21, 28],
    81: [36, 45],
    83: [3, 6, 10, 15, 21, 28],
    84: [1, 3, 6, 10, 15, 21, 28],
    85: [21, 28, 36],
    100: [15, 21, 28, 36],
    109: [28, 36, 45],
    110: [10, 15, 21, 28, 36],
    116: [6, 10, 15, 21, 28, 36],
    119: [3, 6, 10, 15, 21, 28, 36],
    120: [1, 3, 6, 10, 15, 21, 28, 36],
    121: [55, 66],
    130: [21, 28, 36, 45],
    136: [36, 45, 55],
    144: [66, 78],
    145: [15, 21, 28, 36, 45],
    155: [10, 15, 21, 28, 36, 45],
    161: [6, 10, 15, 21, 28, 36, 45],
    164: [3, 6, 10, 15, 21, 28, 36, 45],
    165: [1, 3, 6, 10, 15, 21, 28, 36, 45],
    166: [45, 55, 66],
    169: [78, 91],
    185: [21, 28, 36, 45, 55],
    196: [91, 105],
    199: [55, 66, 78],
    200: [15, 21, 28, 36, 45, 55],
    202: [36, 45, 55, 66],
    210: [10, 15, 21, 28, 36, 45, 55],
    216: [6, 10, 15, 21, 28, 36, 45, 55],
    219: [3, 6, 10, 15, 21, 28, 36, 45, 55],
    220: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55],
    225: [105, 120],
    230: [28, 36, 45, 55, 66],
    235: [66, 78, 91],
    244: [45, 55, 66, 78],
    251: [21, 28, 36, 45, 55, 66],
    256: [120, 136],
    266: [15, 21, 28, 36, 45, 55, 66],
    274: [78, 91, 105],
    276: [10, 15, 21, 28, 36, 45, 55, 66],
    280: [36, 45, 55, 66, 78],
    282: [6, 10, 15, 21, 28, 36, 45, 55, 66],
    285: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66],
    286: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66],
    289: [136, 153],
    290: [55, 66, 78, 91],
    308: [28, 36, 45, 55, 66, 78],
    316: [91, 105, 120],
    324: [153, 171],
    329: [21, 28, 36, 45, 55, 66, 78],
    335: [45, 55, 66, 78, 91],
    340: [66, 78, 91, 105],
    344: [15, 21, 28, 36, 45, 55, 66, 78],
    354: [10, 15, 21, 28, 36, 45, 55, 66, 78],
    360: [6, 10, 15, 21, 28, 36, 45, 55, 66, 78],
    361: [105, 120, 136],
    363: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78],
    364: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78],
    371: [36, 45, 55, 66, 78, 91],
    394: [78, 91, 105, 120],
    395: [55, 66, 78, 91, 105],
    399: [28, 36, 45, 55, 66, 78, 91],
    400: [190, 210],
    409: [120, 136, 153],
    420: [21, 28, 36, 45, 55, 66, 78, 91],
    435: [15, 21, 28, 36, 45, 55, 66, 78, 91],
    440: [45, 55, 66, 78, 91, 105],
    441: [210, 231],
    445: [10, 15, 21, 28, 36, 45, 55, 66, 78, 91],
    451: [6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91],
    452: [91, 105, 120, 136],
    454: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91],
    455: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91],
    460: [66, 78, 91, 105, 120],
    476: [36, 45, 55, 66, 78, 91, 105],
    484: [231, 253],
    504: [28, 36, 45, 55, 66, 78, 91, 105],
    514: [105, 120, 136, 153],
    515: [55, 66, 78, 91, 105, 120],
    525: [21, 28, 36, 45, 55, 66, 78, 91, 105],
    529: [253, 276],
    530: [78, 91, 105, 120, 136],
    540: [15, 21, 28, 36, 45, 55, 66, 78, 91, 105],
    550: [10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105],
    556: [6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105],
    559: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105],
    560: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105],
    571: [171, 190, 210],
    576: [276, 300],
    580: [120, 136, 153, 171],
    596: [36, 45, 55, 66, 78, 91, 105, 120],
    605: [91, 105, 120, 136, 153],
    624: [28, 36, 45, 55, 66, 78, 91, 105, 120],
    625: [300, 325],
    631: [190, 210, 231],
    645: [21, 28, 36, 45, 55, 66, 78, 91, 105, 120],
    650: [136, 153, 171, 190],
    651: [55, 66, 78, 91, 105, 120, 136],
    660: [15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120],
    670: [10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120],
    676: [6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120],
    679: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120],
    680: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120],
    683: [78, 91, 105, 120, 136, 153],
    685: [105, 120, 136, 153, 171],
    694: [210, 231, 253],
    696: [45, 55, 66, 78, 91, 105, 120, 136],
    724: [153, 171, 190, 210],
    729: [351, 378],
    732: [36, 45, 55, 66, 78, 91, 105, 120, 136],
    749: [66, 78, 91, 105, 120, 136, 153],
    760: [28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    770: [120, 136, 153, 171, 190],
    776: [91, 105, 120, 136, 153, 171],
    781: [21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    784: [378, 406],
    796: [15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    802: [171, 190, 210, 231],
    804: [55, 66, 78, 91, 105, 120, 136, 153],
    806: [10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    812: [6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    815: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    816: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136],
    829: [253, 276, 300],
    841: [406, 435],
    849: [45, 55, 66, 78, 91, 105, 120, 136, 153],
    854: [78, 91, 105, 120, 136, 153, 171],
    860: [136, 153, 171, 190, 210],
    875: [105, 120, 136, 153, 171, 190],
    884: [190, 210, 231, 253],
    885: [36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    900: [435, 465],
    901: [276, 300, 325],
    913: [28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    920: [66, 78, 91, 105, 120, 136, 153, 171],
    934: [21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    949: [15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    955: [153, 171, 190, 210, 231],
    959: [10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    961: [465, 496],
    965: [6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    966: [91, 105, 120, 136, 153, 171, 190],
    968: [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    969: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153],
    970: [210, 231, 253, 276],
    975: [55, 66, 78, 91, 105, 120, 136, 153, 171],
    976: [300, 325, 351],
    980: [120, 136, 153, 171, 190, 210]
}

# pprint(master_array)


def checkio(n):
    return master_array.get(n, [])

checkio(64) == [15, 21, 28]
checkio(371) == [36, 45, 55, 66, 78, 91]
checkio(225) == [105, 120]
checkio(882) == []
print("Done!")


# end of file