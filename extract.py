#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""Soundcloud Cover Artwork URL Extractor.

"""

from html.parser import HTMLParser
import sys
import urllib.request


class SoundcloudImageExtractor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.image = None

    def extract(self, source):
        self.feed(source)
        return self.image

    def handle_starttag(self, tag, attrs):
        if tag != 'meta':
            return

        attr = dict(attrs)

        if 'property' in attr:
            prop = attr['property']

            if prop == 'og:image' and 'content' in attr:
                content = attr['content']
                self.image = content


if len(sys.argv) != 2:
    print('Usage: {} URL'.format(sys.argv[0]))
    exit(1)

url = sys.argv[1]

request = urllib.request.Request(url)
with urllib.request.urlopen(request) as response:
    html = response.read()
    source = html.decode('utf-8')

    parser = SoundcloudImageExtractor()

    image = parser.extract(source)
    if not image:
        print('Failed to extract image URL from given page.')
        exit(1)

    print(image)
