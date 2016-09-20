"Count the 'striped' words (words with alternating vowel and consonants"

import re

VOWELS = "AEIOUY"


def striped(word):
    """Check for alternating vowel/non-vowel in uppercased 'word'."""

    if len(word) < 2:
        return 0

    word = list(word)

    flag = (word.pop(0) in VOWELS)

    for c in word:
        if flag:
            flag = (c in VOWELS)
            if flag:
                return 0
        else:
            flag = (c in VOWELS)
            if not flag:
                return 0
    return 1


def checkio(s):
    """Count striped words in s."""
    words = re.split("[^A-Z]+", s.upper())
    count = 0
    for word in words:
        count += striped(word)
    return count


assert checkio("My name is ...") == 3
assert checkio("Hello world") == 0
assert checkio("A quantity of striped words.") == 1, "Only of"
assert checkio("Dog,cat,mouse,bird.Human.") == 3
print("Done!")
