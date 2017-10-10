#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import re
from xml.etree.ElementTree import parse, tostring


def print_kv(node):
    key = node.attrib.get('name')
    value = node.text

    if value:
        value = re.sub('[ \t\n]+', ' ', value)
    else:
        value = re.sub(r'[\n \t\r]+', ' ', tostring(child, "utf-8").decode())
        value_group = re.match(r'<(string|item)[^>]*>(.*)</(string|item)>', value)
        if value_group:
            value = value_group.group(2)
    print('%s,%s' % (key, value))


if sys.argv[1] is None:
    xml = input("没有指定源xml文件. 请重新输入一个 : ")
else:
    xml = sys.argv[1]

doc = parse(xml).getroot()

for child in doc:
    if child.tag == 'string' or child.tag == 'item':
        print_kv(child)

    elif child.tag == 'string-array' or child.tag == 'plurals':
        for i in child.findall('item'):
            print_kv(i)





    # if child.tag == 'string':
    #     child_is_none = child.text is None
    #
    #     value = re.sub(r'[\n \t\r]+', ' ', tostring(child, "utf-8").decode() if child_is_none else str(child.text))
    #
    #     if child_is_none:
    #         g = re.match(r'<string[^>]*>(.*)</string>', value)
    #         if g:
    #             value = g.group(1)
    #         else:
    #             value = ''
    #
    # elif child.tag == 'string-array':
    #     items = []
    #     for i in child.findall('item'):
    #         items.append(i.text)
    #
    #     value = '|||'.join(items)





