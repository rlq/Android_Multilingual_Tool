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
        s,>>,>,g;
        /translatable="false"/{d; t end};

        # or it will not be saved.</string>     删  整行
        /<string/ !{/<\/string>/{d; t end}};

        # <string name="three">33333</string>     删   33333
        /<string.*<\/string>/ { s,\(<string[^>]*>\).*<\/string>,\1</string>,; t end};
        /<item.*<\/item>/     { s,\(<item[^>]*>\).*<\/item>,\1</item>,;       t end};

        # <string name="gps_dialog_phone">Disconnect to the phone   删  Disconnect to the phone, 再加</string>
        /<string/{/<\/string>/ !{s,\(<string[^>]*>\).*,\1</string>,; t end}};
        /<item/{/<\/item>/     !{s,\(<item[^>]*>\).*,\1</item>,; t end}};


        # <string name="info_tips">Please enter your
        # data to make the \n movement data
        # more accurate</string>
        /<\?xml\|<resources>\|<\/resources>\|<!--\|^[ \t\n\r]*$/!d




        : end


#        /<string.*<\/string>\|<string-array/ !s,\(<string[^>]*>\).*$,\1</string>,;
#        /<string.*<\/string>/ !s,^.*</string>.*,</string>,;
#        /^<\/string>$/d;
#
#        /^[ \t]*$\|resources\|-->/!{/string/!d};
#
#        s,>>,>,g;
#        s,\(<string[^>]*>\).*</string>,\1</string>,g;
#        /translatable="false"/d
    ' $f > $t/$f
done

#
#    <plurals name="health_dev_session_load_success2" translatable="false">
#        <item quantity="one" name="health_dev_session_load_success02">%d activity has been imported</item>
#        <item quantity="other" name="health_dev_session_load_success12">%d activities have been imported</item>
#    </plurals>
#上面这个例子sed不好处理, 放弃sed. 用python重写.