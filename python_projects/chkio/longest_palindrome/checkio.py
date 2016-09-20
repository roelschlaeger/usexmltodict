# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/the-longest-palindromic/

# http://articles.leetcode.com/longest-palindromic-substring-part-i
# http://articles.leetcode.com/longest-palindromic-substring-part-ii


def preprocess(s):
    """Preprocess the input string in preparation for the algorithm."""

    n = len(s)
    if n == 0:
        return "^$"

    out = ["^"]
    for c in s:
        out.append("#")
        out.append(c)
    out.append("#$")
    return "".join(out)


def longest_palindromic(s):
    """Find the longest palindrome in the string s using the Manacher
algorithm."""

    t = preprocess(s)

    n = len(t)
    p = [0] * n

    c = 0
    r = 0

    for i in range(1, n - 1):

        i_mirror = 2 * c - i

        if r > i:
            p[i] = min(r - i, p[i_mirror])
        else:
            p[i] = 0

        # attempt to expand palindrome centered at i
        while((t[i + 1 + p[i]]) == (t[i - 1 - p[i]])):
            p[i] += 1

        # if palindrome centered at i expands past r
        # adjust the center based on the palindrome
        if (i + p[i]) > r:
            c = i
            r = i + p[i]

    # find the maximum element in p
    maxlen = 0
    centerindex = 0
    for i in range(1, n):
        if p[i] > maxlen:
            maxlen = p[i]
            centerindex = i

    left = (centerindex - 1 - maxlen) / 2
    right = left + maxlen
    result = s[left:right]
    return result


longest_palindromic("aba")
longest_palindromic("abba")
longest_palindromic("abcba")
longest_palindromic("leftabcba")
longest_palindromic("abcbaright")
longest_palindromic("trashablewasiereisawelbajunk")
#
