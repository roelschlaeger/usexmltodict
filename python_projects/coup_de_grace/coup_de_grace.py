TRANSLATE_PAIRS = {
    'B': '1',
    'Z': '0',
    'X': '2',
    'D': '3',
    'V': '4',
    'F': '5',
    'T': '6',
    'H': '7',
    'R': '8',
    'J': '9',
}

import string
keys = "".join(TRANSLATE_PAIRS.keys())
values = "".join(TRANSLATE_PAIRS.values())
TABLE = string.maketrans(keys, values)

result = "XXDDD\nXDRRR".translate(TABLE)
print(result)

result = string.printable.translate(TABLE)
print(result)
