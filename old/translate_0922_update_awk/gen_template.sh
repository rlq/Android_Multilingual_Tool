#!/bin/bash

t="../template"
s="source"

rm -rf template
test -d template || mkdir template

cd $s

for f in `find . -type f -name "*string*.xml"`
do
    dir=`dirname $f`
    echo "$t/$dir"
    test -d $t/$dir || mkdir -p $t/$dir
    gsed '
        /<string.*<\/string>\|<string-array/ !s,\(<string[^>]*>\).*$,\1</string>,;
        /<string.*<\/string>/ !s,^.*</string>.*,</string>,;
        /^<\/string>$/d;

        /^[ \t]*$\|resources\|-->/!{/string/!d};
        
        s,>>,>,g; 
        s,\(<string[^>]*>\).*</string>,\1</string>,g;
        /translatable="false"/d
    ' $f > $t/$f
done
        #s,\(<\(string\)[^>]*>\)[^\(</string\)]*$,\1</\2>,;

        #/>[^<]*$/ s,>.*,>,;
        #/^[^>]*</ s,^\( \t\)*.*<,\1<,;
        #/^[^><]*[a-zA-Z]+$/d;
