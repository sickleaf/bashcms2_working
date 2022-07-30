#!/bin/bash
source "$(dirname $0)/conf"
exec 2>> "$logdir/$(date +%Y%m%d).$(basename $0)"

sed 's/%2C/\n/g' <<< ${QUERY_STRING}     |
nkf --url-input                     |
sed -e '1s/keywords=//' -e 's/^[ 　]*//' -e 's/[ 　]*$//' |
nkf -w16B0                          |
xxd -plain                          |
tr -d '\n'                          |
sed 's/..../\&#x&;/g'               |
sed 's/\&#x000a;/\n/g'              |
awk '{print "<a href=\"/key.cgi?key="$1 "\">" $1 "</a>" }'	|
#awk '{print "<span onclick=\"keyword(@@@$1@@@)\">" $1 "</span>" }'	|
sed 's/@@@/\x47/g'					|
sed '1iContent-Type: text/html\n'
