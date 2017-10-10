#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import re


template_dir = 'template'
source_dir = 'source'
result_dir = 'target'
language_dir = 'language'
app_name = None
select_lang = None

if len(sys.argv) >= 2:
    app_name = sys.argv[1]

if len(sys.argv) >= 3:
    select_lang = sys.argv[2]


def usage():
    print("""
    %s       
      先找要翻译的template目录, 再找准备好的language文件. 完成翻译, 在target目录中生成翻译好的xml.

    -h       查看帮助文档

    argv1    选择APP的template目录.  如: fitness
    argv2    选择要翻译成什么语言.  如: spanish
    """ % sys.argv[0])

    exit(1)


def get_app_name():
    n = 0
    app_list = []

    print('-------------------------------------')
    print('可选择的APP tempalte:')

    for dir in os.listdir(template_dir):
        print('    %d : %s' % (n, dir))
        app_list.append(dir)
        n += 1
    print('-------------------------------------')
    app_index = input('你选择哪个APP template, 输入前面数字即可: ')

    if n > 0:
        return app_list[int(app_index)]
    else:
        print('找不到模板template!')
        exit(1)


def get_lang():
    n = 0
    print('\n-------------------------------------')
    print('可以翻译成哪些语言:')
    print(os.path.join(language_dir, app_name))
    lang_list = find_lang_list(os.path.join(language_dir, app_name))

    for lang in lang_list:
        print('    %d : %s' % (n, lang))
        n += 1
    print('-------------------------------------')
    select_lang_index = input('要翻译成什么语言, 输入前面的数字即可: ')

    if n > 0:
        return lang_list[int(select_lang_index)]
    else:
        print('找不到可用的翻译language文件!')
        exit(1)


def find_lang_list(app_language_dir):
    lang_list = []
    for dir in os.listdir(app_language_dir):
        if os.path.isdir(os.path.join(app_language_dir, dir)):
            find_lang_list(os.path.join(app_language_dir, dir))
        elif os.path.isfile(os.path.join(app_language_dir, dir)):
            lang_group = re.match(r'^([a-zA-Z]+)-.*.xml', dir)
            if lang_group and lang_group.group(1) not in lang_list:
                lang_list.append(lang_group.group(1))

    return lang_list


def load_language(load_lang_subfile):
    lang_kv = {}
    for file in os.listdir(load_lang_subfile):

        if os.path.isdir(os.path.join(load_lang_subfile, file)):
            load_lang_subfile = os.path.join(load_lang_subfile, file)
            load_language(os.path.join(load_lang_subfile, file))
        elif os.path.isfile(os.path.join(load_lang_subfile, file)):
            lang_group = re.match(r'([a-zA-Z]+)-(.*).xml', file)
            if lang_group:
                stings_name = lang_group.group(2)
            else:
                continue

            if lang_kv.get(lang_group.group(2)) is None:
                lang_kv[lang_group.group(2)] = {}

            if lang_group.group(1) == select_lang:
                lang_fd = open(os.path.join(load_lang_subfile, file), 'r')
                for line in lang_fd:
                    if len(line.split('@', 1)) == 2:
                        (k, v) = line.split('@', 1)
                        lang_kv[stings_name][k] = v.strip()
    return lang_kv


def write_target_xml(content, target_xml):
    dir = re.sub(r'%s[^/]*$' % os.sep, '', target_xml)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    target_xml_fd = open(target_xml, 'w')
    target_xml_fd.write(content)
    target_xml_fd.close()


def translate():
    lang_kv = load_language(os.path.join(language_dir, app_name))

    for template in os.listdir(os.path.join(template_dir, app_name)):
        content = ''
        template_fd = open(os.path.join(template_dir, app_name, template), 'r')
        strings_name = re.sub('.xml', '', template)

        for line in template_fd:
            key = ''
            key_group = re.match(r'.*string.*name="([^"]+)"', line)
            if key_group:
                key = key_group.group(1)

            if 'string-array' in line and key in lang_kv.get(strings_name):
                items_xml = ''
                item_line_head = ''
                spaces = re.match(r'^([ \t]*)', line)
                if spaces:
                    item_line_head = spaces.group(1)

                items = lang_kv.get(strings_name).get(key).split('|||')

                for item in items:
                    items_xml += '\n%s    <item>%s</item>' % (item_line_head, item)
                items_xml += '\n%s' % item_line_head

                content += re.sub(r'> *</', ">%s</" % items_xml, line)

            elif 'string' in line and key in lang_kv.get(strings_name):
                string_list = re.split(r'>.*</', line)

                content += string_list[0] + '>' + lang_kv.get(strings_name).get(key) + '</' + string_list[1]
            else:
                content += line

        write_target_xml(content, os.path.join(result_dir,  app_name, template))


if app_name == '-h':
    usage()

if app_name is None or not os.path.isdir(os.path.join(template_dir, app_name)):
    app_name = get_app_name()


if select_lang is None or not os.path.isdir(os.path.join(language_dir, app_name)):
    select_lang = get_lang()


translate()



