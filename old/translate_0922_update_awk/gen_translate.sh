#!/bin/bash

t="template"
s="source"
r="target"
l="language"

template=$1
language=$2

usage(){
    echo "
    $0     先找要翻译的template目录, 再找准备好的language文件. 完成翻译, 在target目录中生成翻译好的xml.

    -h     查看帮助文档

    \$1    选择APP的template目录. 如: fit_res
    \$2    选择要翻译成什么语言.  如: spanish
    "

    exit 0
}

translate(){
    template=$1
    language=$2

    for temp_file in `find $t/$template -type f -name "*string*.xml"`
    do
        lang_file=`echo "$temp_file" | sed 's/^'"$t"'/'"$l"'/'; s,/\([^/]+\)$,/'"$language"'-\1,`
        target_file=``
        test -f $lang_file || { echo "$lang_file 不存在!!!"; continue; }

        
    done
}

if [[ $1 == "-h" ]];then
    usage
fi

test -d $t || { echo "$t 不存在!"; exit 1; }

if test -z $1 || ! test -d $t/$1 ; then
    n=1
    echo "------------------------------"
    echo "可选择的APP tempalte:"
    for dir in `find $t -type d -depth 1 | sed -n '/\//s,.*/\(.*\),\1,p'`
    do
        echo "   $n : $dir"
        temp[$n]=$dir
        n=$[ n + 1 ]
    done
    echo "------------------------------"
    echo -n "你选择哪个APP template, 输入前面数字即可: "
    read template_n
    template=${temp[$template_n]} 
fi

test -z $template && { echo "找不到模板template!"; exit 1; }

if test -z $2 || ! test -d $l/$template ; then
    n=1
    echo
    echo "------------------------------"
    echo "可以翻译成哪些语言:"
    for language in `find $l/$1 -type f -name "*-*string*.xml" 2>/dev/null | sed 's,.*/\(.*\)-.*.xml,\1,' | sort | uniq`
    do
        echo "    $n : $language"
        lang[$n]=$language
        n=$[ n + 1 ]
    done
    echo "------------------------------"
    echo -ne "\n要翻译成什么语言, 输入前面的数字即可: "
    read language_n
    language=${lang[$language_n]}
fi

test -z $language && { echo "找不到可用的翻译language文件!"; exit 1; }

echo
echo "现在将把 $template 翻译成 $language."
echo "翻译好的 xml文件 在 target目录下面."
echo


