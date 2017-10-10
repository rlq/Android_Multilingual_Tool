#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import re
from xml.dom import minidom

from xml.etree.ElementTree import parse, tostring


template_dir = 'template'
source_dir = 'source'

os.system('rm -rf %s' % template_dir)
os.mkdir(template_dir)


def parse_xml(f):
    doc = parse(f)

    for child in doc.getroot():
        if child.tag == 'string' or child.tag == 'string-array':
            attribs = child.attrib
            child.clear()
            child.text = " "
            for k,v in attribs.items():
                child.set(k, v)

    pretty_xml = tostring(doc.getroot(), 'utf-8')
    pretty_xml = minidom.parseString(pretty_xml)

    pretty_xml_text = pretty_xml.toprettyxml(indent="\t")
    template_file = open(re.sub(source_dir, template_dir, f), "w")
    template_file.writelines(pretty_xml_text)
    template_file.close()


def find_source_xml(dir):
    for file in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, file)):
            template_path = re.sub(source_dir, template_dir, os.path.join(dir, file))
            os.mkdir(template_path)
            find_source_xml(os.path.join(dir, file))
        elif os.path.isfile(os.path.join(dir, file)) and re.match(r'.*string.*\.xml', file):
            parse_xml(os.path.join(dir, file))


find_source_xml(source_dir)
