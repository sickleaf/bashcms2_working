#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2>> "$logdir/$(date +%Y%m%d).$(basename $0)"

cat "$datadir/post_list"  |
cut -c 1-7 		|
awk '{print "<a href=\"viewTop.cgi?ym=" $0 "\">" $0 "</a>" }' |
uniq -c 		|
sed -E "s;^ *;;g; s;^([0-9]*) ;\1;g" |
awk -F"<"  '{print "",$2 "(" $1 ")" ,$3 "<br>"}' OFS=\< |
sed "1s;<br>$;;" 	|
tac 			|
sed '1iContent-Type: text/html\n\n<h3>Monthly Archive</h3>'
