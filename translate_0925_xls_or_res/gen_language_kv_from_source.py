#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import re
import os
from xml.etree.ElementTree import parse, tostring
from termcolor import colored

from config import *


def create_language_dir(file):
    dir = re.sub(r'/[^/]*$', '', file)
    if not os.path.isdir(dir):
        os.makedirs(dir)
#
#
# def print_kv(node):
#     key = node.attrib.get('name')
#     value = node.text
#     # print(tostring(node, "utf-8", short_empty_elements=False, method='html'))
#
#     if value is None:
#         value = tostring(child, "utf-8").decode('utf8')
#
#         value_group = re.match(r'<(string|item)[^>]*>(.*)</(string|item)>', value)
#         if value_group:
#             value = value_group.group(2)
#         else:
#             value = ''
#
#     value = re.sub(r'^"|"$', '', value)
#
#     if '/values/' in language_kv_file:
#         print_value = re.sub('\n', enter_tag, value)
#         print('%s,%s' % (key, print_value))
#
#     return '    \'%s\': r""" %s """,\n' % (key, value)


def input_xml_file_path(d):
    _n = 1
    f_list = ['', ]

    if not os.path.exists(d):
        print(colored('%s 文件不存在!!!' % d, 'red'))
        exit(1)

    if not re.match('^%s' % source_dir, d):
        print(colored('参数路径应该是以 %s/ 开始的相对路径.' % source_dir, 'red'))
        exit(1)

    if os.path.isdir(d):
        for f in os.listdir(d):
            if os.path.isfile(os.path.join(d, f)) and '.xml' in f and 'string' in f:
                print('    %d : %s' % (_n, f))
            elif os.path.isdir(os.path.join(d, f)):
                print(colored('    %d : %s' % (_n, f), 'cyan'))
            else:
                continue
            f_list.append(f)
            _n += 1
    elif os.path.isfile(d) and '.xml' in d and 'string' in d:
        return d
    else:
        print(colored('%s 不是XML文件!!!' % d, 'red'))
        exit(1)

    select_f_index = int(input('输入你选择的文件编号. 蓝色是目录, 白色是可能合适的XML文件. : '))
    if os.path.isdir(os.path.join(d, f_list[select_f_index])):
        return input_xml_file_path(os.path.join(d, f_list[select_f_index]))
    elif os.path.isfile(os.path.join(d, f_list[select_f_index])):
        return os.path.join(d, f_list[select_f_index])


if __name__ == '__main__':
    xml = ''
    if len(sys.argv) < 2:
        xml = input_xml_file_path(source_dir)
    else:
        xml = input_xml_file_path(sys.argv[1])

    if source_dir not in xml:
        print(colored('应该使用source XML文件!', 'red'))
        exit(1)

    language_kv_file = re.sub(source_dir, language_dir, re.sub(r'\.xml$', '.py', xml))
    create_language_dir(language_kv_file)

    kv_content = '{\n'
    enter_flag = ''   # 标识<string> <item> 换行的情况

    with open(xml, 'r') as xml_fd:
        for line in xml_fd:
            for k in k_list:
                if '<%s ' % k in line and '</%s>' % k in line:
                    matchobj = re.match(r'.*<%s .*name="([^"]*)"[^>]*>(.*)</%s>.*' % (k, k), line)
                    if matchobj:
                        kv_content += '    \'%s\': r""" %s """,\n' % (matchobj.group(1), matchobj.group(2))
                    break

                elif '<%s ' % k in line and '</%s>' % k not in line:
                    matchobj = re.match(r'.*<%s .*name="([^"]*)"[^>]*>(.*)' % k, line)
                    if matchobj:
                        kv_content += '    \'%s\': r""" %s \n' % (matchobj.group(1), matchobj.group(2))
                        enter_flag = k
                    break

                elif enter_flag != '' and '<%s ' % k not in line and '</%s>' % k in line:
                    matchobj = re.match(r'(.*)</%s>.*' % k, line)
                    if matchobj:
                        kv_content += '%s """,\n' % matchobj.group(1)
                    enter_flag = ''
                    break

                elif enter_flag and '<%s ' % k not in line and '</%s>' % k not in line and enter_flag == k:
                    kv_content += line
                    break

    kv_content += '}\n'

    with open(language_kv_file, 'wb') as language_kv_file_fd:
        print(colored('生成 : %s' % language_kv_file, 'green'))
        language_kv_file_fd.write(kv_content.encode('utf-8'))
