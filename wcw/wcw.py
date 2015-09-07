#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import re
import getopt
import urllib2
import logging

from collections import namedtuple
from xml.dom import minidom
from termcolor import colored

KEY = "E0F0D336AF47D3797C68372A869BDBC5"
URL = "http://dict-co.iciba.com/api/dictionary.php"
TAG = namedtuple('TAG', 'value color')
TAG_DICT = {
    'ps': TAG('[%s]', 'green'),
    'fy': TAG('%s', 'green'),
    'orig': TAG('ex. %s', 'blue'),
    'trans': TAG('   %s', 'cyan'),
    'pos': TAG('%s'.ljust(12), 'green'),
    'acceptation': TAG('%s', 'yellow')
}

def get_response(word):
    try:
        url = URL + '?key=' + KEY + '&w=' + word
        response = urllib2.urlopen(url)
    except urllib2.URLError:
        logging.error("哎呦，出错了！")
        return
    return response

def read_xml(xml):
    dom = minidom.parse(xml)
    return dom.documentElement

def show(node):
    if not node.hasChildNodes():
        if node.nodeType == node.TEXT_NODE and node.data != '\n':
            tag_name = node.parentNode.tagName
            content = node.data.replace('\n', '')
            if tag_name in TAG_DICT.keys():
                tag = TAG_DICT[tag_name]
                print colored(tag.value % content, tag.color)
    else:
        for e in node.childNodes:
            show(e)
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],["help"])
    except getopt.GetoptError as e:
        pass

    pattern = r'[\w.]+'
    match = re.findall(pattern, " ".join(args))

    word = "%20".join(match)
    response = get_response(word)
    if not response:
        return

    root = read_xml(response)

    show(root)


if __name__ == "__main__":
    main()
