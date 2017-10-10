#!/bin/bash

replace=${1/.txt/}
#replace=spanish
#replace=french
#replace=german
#replace=japanese

if [[ -z $replace ]];then
    echo
    echo "需要一个参数指定翻译对照文件."
    echo
    exit 1
fi

if ! test -f $replace.txt ;then
    echo 
    echo "$replace.txt 不存在. 需要重新指定一个可用的翻译对照文件."
    echo 
    exit 1
fi

for f in `find . -type f -name "*strings.xml"`
do
    new_f=`echo "$f" | sed 's/.xml/-2.xml/'`
    printf "%-50s ---> %s\n" $f $new_f  
    awk -F'[@><]' 'BEGIN{OFS="@"}{
    if(NR==FNR){
        r[$1]=$2
        }else{
            tmp=$3;
            if(r[$3]==""){
                r[$3]=" "
            };
            gsub(/>.*</,">"r[$3]"<");
            if($3==" "){
                split(tmp, A, /^[^a-zA-Z0-9]*|[^a-zA-Z0-9]+$/);
                if(r[A[1]]!=" " && r[A[1]]!="") {
                    gsub(/> </,">"r[A[1]]"<")
                }else if(r[A[2]]!=" " && r[A[2]]!="") {
                    gsub(/> </,">"r[A[2]]"<")
                }else{
                    gsub(/> </,">#:#:#:#"tmp"###<")
                }
            };
            print
        }
    }' $replace.txt $f > $new_f
    grep '#:#:#:#' $new_f > $new_f.grep.txt
done
