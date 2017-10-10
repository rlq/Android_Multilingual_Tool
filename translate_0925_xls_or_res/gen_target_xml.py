#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import sys

from termcolor import colored

from config import *

template_dir = 'template'
source_dir = 'source'
result_dir = 'target'
language_dir = 'language'
app_name = None
select_lang = None


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
    n = 1
    app_list = []

    print('-------------------------------------')
    print('可选择的APP tempalte:')

    for dir in os.listdir(template_dir):
        print('    %d : %s' % (n, dir))
        app_list.append(dir)
        n += 1
    print('-------------------------------------')
    app_index = input(colored('你选择哪个APP template, 输入前面数字即可: ', 'green'))

    app_index = int(app_index) - 1
    if n > 0:
        return app_list[app_index]
    else:
        print('找不到模板template!')
        exit(1)


def get_lang():
    n = 1
    print('\n-------------------------------------')
    print('可以翻译成哪些语言:')
    lang_list = find_lang_list(os.path.join(language_dir, app_name))

    for lang in lang_list:
        print('    %d : %s' % (n, lang))
        n += 1
    print('-------------------------------------')
    select_lang_index = input(colored('要翻译成什么语言, 输入前面的数字即可: ', 'green'))

    select_lang_index = int(select_lang_index) - 1
    if n > 0:
        return lang_list[select_lang_index]
    else:
        print('找不到可用的翻译language文件!')
        exit(1)


def find_lang_list(app_language_dir):
    lang_list = []
    for dir in os.listdir(app_language_dir):
        if os.path.isdir(os.path.join(app_language_dir, dir)) and 'values-' in dir:
            lang_list.append(re.sub('values-', '', dir))

    return lang_list


def load_language(load_lang_subfile):
    lang_kv = {}
    for file in os.listdir(load_lang_subfile):
        if 'string' in file and '.py' in file:
            string_name = re.sub('\.py', '', file)

            with open(os.path.join(load_lang_subfile, file), 'r') as lang_kv_file_fd:
                lang_kv[string_name] = eval(lang_kv_file_fd.read().encode('utf-8'))

    return lang_kv


def write_target_xml(content, target_xml):
    dir = re.sub(r'%s[^/]*$' % os.sep, '', target_xml)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    target_xml_fd = open(target_xml, 'w')
    target_xml_fd.write(content)
    target_xml_fd.close()


def create_target_lang_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


def translate():
    lang_kv = load_language(os.path.join(language_dir, app_name, 'values-%s' % select_lang))

    for template_file in os.listdir(os.path.join(template_dir, app_name, 'values-%s' % select_lang)):
        content = ''
        template_fd = open(os.path.join(template_dir, app_name, 'values-%s' % select_lang, template_file), 'r')
        string_name = re.sub('.xml', '', template_file)

        if lang_kv.get(string_name) is None:
            print(colored('language_kv 文件不存在! : %s' %
                          os.path.join(language_dir, app_name, 'values-%s' % select_lang, template_file), 'red'))
            break

        for line in template_fd:
            if '</string>' not in line and '</item>' not in line:
                content += line
                continue

            key_group = re.match(r'.*(string|item).*name="([^"]+)"', line)
            if key_group:
                key = key_group.group(2)
                language_kv_value = lang_kv.get(string_name).get(key, '').strip()

                string_list = re.split(r'>.*</', line)
                content += string_list[0] + '>' + language_kv_value + '</' + string_list[1]

        target_file = os.path.join(result_dir,  app_name, 'values-%s' % select_lang, template_file)
        print(colored('生成 : %s' % target_file, 'green'))
        write_target_xml(content, target_file)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        app_name = sys.argv[1]

    if len(sys.argv) >= 3:
        select_lang = sys.argv[2]

    if app_name == '-h':
        usage()

    if app_name is None or not os.path.isdir(os.path.join(template_dir, app_name)):
        app_name = get_app_name()

    if select_lang is None or select_lang not in find_lang_list(os.path.join(language_dir, app_name)):
        select_lang = get_lang()

    print()
    translate()



