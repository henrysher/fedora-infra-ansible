#!/usr/bin/env python
""" Reads a string from stdin and prints it to stdout with irc colors

:license: LGPLv2+
:author: Ralph Bean <rbean@redhat.com>
"""

import sys

mirc_colors = {
    "white": 0,
    "black": 1,
    "blue": 2,
    "green": 3,
    "red": 4,
    "brown": 5,
    "purple": 6,
    "orange": 7,
    "yellow": 8,
    "light green": 9,
    "teal": 10,
    "light cyan": 11,
    "light blue": 12,
    "pink": 13,
    "grey": 14,
    "light grey": 15,
}

mapping = {
    'RECOVERY': 'green',
    'OK': 'green',
    'ACKNOWLEDGEMENT': 'yellow',
    'UNKNOWN': 'purple',
    'WARNING': 'teal',
    # 'red' probably makes the most sense here, but it behaved oddly
    'PROBLEM': 'brown',
    'CRITICAL': 'brown',
}


def markup(string, color):
    return "\x02\x03%i%s\x03\x02" % (mirc_colors[color], string)


def colorize(word):
    suffix = ''
    if word.endswith(':'):
        word, suffix = word[:-1], word[-1]

    if word in mapping:
        word = markup(word, mapping[word])

    return word + suffix


if __name__ == '__main__':
    lines = sys.stdin.readlines()
    for line in lines:
        print " ".join([colorize(word) for word in line.strip().split()])
