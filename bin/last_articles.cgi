#!/bin/bash
source "$(dirname $0)/conf"
exec 2>> "$logdir/$(date +%Y%m%d).$(basename $0)"

num=$(tr -dc '0-9' <<< ${QUERY_STRING})
[ -z "$num" ] && num=10

tac "$datadir/post_list"		|
head -n "$num"				|
awk '{print $3}'                        |
xargs -I@ cat "$datadir/@/link_date"    |
sed 's;$;<br />;'			|
sed '1iContent-Type: text/html\n\n<h2>Recent posts</h2>'
