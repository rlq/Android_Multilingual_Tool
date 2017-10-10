#!/bin/bash

strings=$1
if [[ -z $strings ]];then
  echo "请输入需要生成的strings.xml文件"
  read strings
fi

test -f $strings || { echo "$strings 不存在"; exit 1; }

gsed -r '/<string.*<\/string>|<string-array/!d;s/.*name="(.*)">([^<]*)<.*/\1,\2/; s/.*<item>(.*)<\/item>/\1/' $strings
