#!/bin/bash

#sed算是整理string. 再用
awk -F'[@><]+' 'BEGIN{OFS="@"}{if(NR==FNR){r[$1]=$2} else{if(r[$3]==""){tmp=$3;r[$3]=" "};gsub(/>.*</,">"r[$3]"<");if($3==" "){split(tmp, A, /, */);gsub(/> </,">"r[A[2]]"<")};print}}' replace.txt tts_strings.xml
#处理string文件.