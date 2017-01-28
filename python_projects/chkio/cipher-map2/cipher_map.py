# https://py.checkio.org/mission/cipher-map2/

"""Decipher passwords using 4x4 grid."""

from __future__ import print_function


def rot90(m):
    """Rotate the 4x4 matrix m 90 degrees CW."""
    return [[m[row][col] for row in range(3, -1, -1)] for col in range(4)]


def recall_password(grill, password):
    """Decipher passwords using 4x4 grid."""
    pw = "".join(password)
    mask = [[column == 'X' for column in row] for row in grill]

    cleartext = ""
    for _ in range(4):
        cleartext += "".join(
            ([pw[x] for x in range(16) if mask[x // 4][x % 4]])
        )
        mask = rot90(mask)

    return cleartext

###############################################################################

if __name__ == '__main__':

    assert recall_password(('X...', '..X.', 'X..X', '....'), ('itdf', 'gdce', 'aton', 'qrdi')) == 'icantforgetiddqd'
    assert recall_password(('....', 'X..X', '.X..', '...X'), ('xhwc', 'rsqx', 'xqzz', 'fyzr')) == 'rxqrwsfzxqxzhczy'
