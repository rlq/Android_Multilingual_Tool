#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import re

from termcolor import colored


template_dir = 'template'
source_dir = 'source'

os.system('rm -rf %s' % template_dir)
os.system('mkdir %s' % template_dir)


def traversal_source_dir(dir):
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)):
            if re.match(r'.*string.*\.xml$', file):
                gen_template(os.path.join(dir, file))

        elif os.path.isdir(os.path.join(dir, file)):
            traversal_source_dir(os.path.join(dir, file))


def create_template_xml_dir(template_xml_name):
    dir = re.sub('/[^/]*$', '', template_xml_name)
    if not os.path.isdir(dir):
        os.makedirs(dir)


def gen_template(source_xml):
    template_xml_name = re.sub('source', template_dir, source_xml)
    create_template_xml_dir(template_xml_name)

    print('%60s ---> %s' % (source_xml, template_xml_name))

    with open(source_xml, 'r') as sxml_fd:
        template_xml_content = ''
        delete = False
        translatable_false_tag = None

        for line in sxml_fd:
            line = re.sub('>>', '>', line)

            if '@' in line:
                print(colored('@@@@@@ %s' % line.strip(), 'red'))

            if 'translatable="false"' in line:
                translatable_false_tag = re.sub(r'.*<([a-zA-A]+) .*translatable="false".*>.*', r'\1', line).strip()
                if '</%s>' % translatable_false_tag in line:
                    translatable_false_tag = None

            elif translatable_false_tag:
                if '</%s>' % translatable_false_tag in line:
                    translatable_false_tag = None

            elif '<string ' in line and '</string>' in line:
                template_xml_content += re.sub(r'(<string[^>]*>).*</string>', r'\1</string>', line)

            elif '<item ' in line and '</item>' in line:
                template_xml_content += re.sub(r'(<item[^>]*>).*</item>', r'\1</item>', line)

            elif '<string ' in line and '</string>' not in line:
                template_xml_content += re.sub(r'(<string[^>]+>).*', r'\1</string>', line)
                delete = True

            elif '<item ' in line and '</item>' not in line:
                template_xml_content += re.sub(r'(<item[^>]+>).*', r'\1</item>', line)
                delete = True

            elif delete and ('</item>' in line or '</string>' in line):
                delete = False

            elif delete is False and translatable_false_tag is None:
                template_xml_content += line

        with open(template_xml_name, 'w') as template_xml_name_fd:
            template_xml_name_fd.write(template_xml_content)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        traversal_source_dir(source_dir)
    elif len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            gen_template(sys.argv[1])
        else:
            print(colored('%s 不存在!' % sys.argv[1], 'red'))







