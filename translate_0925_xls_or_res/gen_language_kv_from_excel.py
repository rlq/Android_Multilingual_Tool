#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import re
import os
import xlrd

from config import *

from termcolor import colored


def usage():
    print("""
    %s 
        依据翻译excel文件生成language_kv文件.
        需要三个参数.
        
        argv1     excel文件路径
        argv2     app_name(excel工作表名)
        argv3     语言(如: french)
        argv4     是追加还是覆盖?   [n|N|no|NO] 这四个字符是覆盖.  其他任意字符是追加.
    """ % sys.argv[0])

    exit(1)


def check_argv(argv):
    def __get_excel():
        if len(argv) >= 2 and os.path.isfile(argv[1]):
            excel_name = argv[1]
            excel = xlrd.open_workbook(excel_name)
        elif len(argv) >= 2 and not os.path.isfile(argv[1]):
            print(colored('%s 不存在!' % argv[1], 'red'))
            usage()
        else:
            print(colored('需要指定一个EXCEL文件!!!', 'red'))
            usage()
        return excel_name, excel

    def __get_table_name():
        if __excel:
            excel_tables = __excel.sheet_names()
        else:
            print(colored('%s 无法读取!!!' % __excel_name, 'red'))
            usage()

        if len(argv) >= 3 and argv[2] in excel_tables:
            table_name = argv[2]
        else:
            print('-------------------------------------')
            print('可选的APP :')
            n = 0
            for t in excel_tables:
                print('    %d : %s' % (n, t))
                n += 1
            table_name_index = input(colored('你选择哪个APP, 输入前面数字即可: ', 'green'))
            table_name = excel_tables[int(table_name_index)]
        return table_name, __excel.sheet_by_name(table_name)

    def __get_lang_names():
        optional_languages = []
        lang_names = []
        if __table:
            language_names = __table.row_values(0)
            for l in language_names:
                if l != '' and l not in optional_languages and str.lower(l) in lang_map.keys():
                    optional_languages.append(l)
            print(optional_languages)
        else:
            print(colored('%s 无法读取!!!' % __excel_name, 'red'))
            usage()

        if len(argv) >= 4 and argv[3] in optional_languages:
            lang_names = [str.lower(argv[3]), ]
            print(lang_names)
        else:
            print('-------------------------------------')
            print('可选的LANGUAGE :')
            n = 0
            for l in optional_languages:
                print('    %d : %s' % (n, re.sub('\n', '', l)))
                n += 1
            lang_names_index = input(colored('你选择哪个LANGUAGE, 输入前面数字即可(直接回车是所有): ', 'green'))

            if lang_names_index == '':
                lang_names = optional_languages
            else:
                lang_names.append(optional_languages[int(lang_names_index)])

        return lang_names, language_names

    def __get_add_flag():
        if len(argv) >= 5:
            add_flag = argv[4]
        else:
            add_flag = input('y:追加(默认)   n:覆盖  [y|n]: ')

        if add_flag == 'n' or add_flag == 'N' or add_flag == 'no' or add_flag == 'NO':
            return False
        else:
            return True

    if '-h' in argv:
        usage()

    (__excel_name, __excel) = __get_excel()
    (__table_name, __table) = __get_table_name()
    (__lang_names, __language_names) = __get_lang_names()
    __add_flag = __get_add_flag()

    return __excel_name, __excel, __table_name, __table, __lang_names, __language_names, __add_flag


def create_language_kv_dir(file):
    dir = re.sub(r'/[^/]*$', '', file)

    if not os.path.isdir(dir):
        os.makedirs(dir)


def write_language_kv_file(language_kv_file, content):
    language_kv_file_content = ''
    create_language_kv_dir(language_kv_file)

    if add_flag and os.path.isfile(language_kv_file):
        with open(language_kv_file, 'r') as language_kv_file_read_fd:
            for line in language_kv_file_read_fd:
                if line == '}\n' or line == '}':
                    language_kv_file_content += content + '}\n'
                else:
                    language_kv_file_content += line
    else:
        language_kv_file_content = '{\n' + content + '}\n'

    with open(language_kv_file, 'w') as language_kv_file_fd:
        print(colored('%s生成 : %s' % ('追加' if add_flag else '覆盖', language_kv_file), 'green'))
        language_kv_file_fd.write(language_kv_file_content)


def gen_language_file(lang_name):
    print('-------------- %s --------------' % lang_name)
    language_kv_file = ''
    short_language = lang_map.get(str.lower(lang_name))
    files_content = {}

    col = 0
    for execl_lang in language_names:
        if str.lower(execl_lang) == lang_name:
            break
        col += 1

    if col == table.ncols:
        exit(1)

    keys = table.col_values(0)
    values = table.col_values(col)

    i = 0
    for key in keys:
        if i == 0 or key == '':
            i += 1
            continue

        if key != '':
            if re.match(r'\(.*/.*\)', key):
                g = re.match(r'\((.*)/(.*)\)', key)
                app_name = str.lower(g.group(1))
                language_kv_file = g.group(2)

                if files_content.get(app_name) is None:
                    files_content[app_name] = {}

            elif re.match(r'\([^/]*\)', key):
                g = re.match(r'\(([^/]*)\)', key)
                app_name = table_name
                language_kv_file = g.group(1)

                if files_content.get(app_name) is None:
                    files_content[app_name] = {}

            else:
                if language_kv_file == '':
                    i += 1
                    print(colored('execel A列中没有找到 (xxxxxx) 配置项 : 第 %d 行' % i, 'red'))
                    exit(1)
                else:
                    string_name = language_kv_file

                if files_content.get(app_name) is None \
                        or files_content.get(app_name).get(string_name) is None:
                    files_content[app_name][string_name] = ''
                files_content[app_name][string_name] += '    \'%s\': r""" %s """,\n' % (key, re.sub(r'^"|"$', '', str(values[i])))

        i += 1

    for app_name in files_content.keys():
        for string_name in files_content.get(app_name):
            language_kv_file = '%s/%s/values%s/%s.py' % (language_dir, app_name,
                                                         '' if short_language == 'en' else '-%s' % short_language,
                                                         string_name)
            write_language_kv_file(language_kv_file, files_content.get(app_name).get(string_name))


if __name__ == '__main__':
    (excel_name, excel, table_name, table, lang_names, language_names, add_flag) = check_argv(sys.argv)

    app_name = table_name

    for lang_name in lang_names:
        gen_language_file(str.lower(lang_name))



