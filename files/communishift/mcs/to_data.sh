#!/bin/bash
echo -n "data:,"
cat $1 | tr '\n' '*' | sed -e 's/*/%0A/g' | sed -e 's/ /%20/g'
echo
