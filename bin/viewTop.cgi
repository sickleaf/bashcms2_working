#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

source "$(dirname $0)/bashcmsFunc.cgi"


pageNum=$(tr -dc 'a-zA-Z0-9='  <<< ${QUERY_STRING} | sed "s;^num=;;g" )

articleListNum=$(grep -c ^ "$datadir/post_list")

HTMLanchor="$(pageAnchorHTML ${articleListNum} ${pageNum} ${articleNum})"


start=$((1+(pageNum-1)*articleNum))
end=$((pageNum*articleNum))

tac "$datadir/post_list"	|
sed -n "${start},${end}p"	|
awk '{print $3}'		|
xargs -I@ cat "$datadir/@/link_date" "$contentsdir/@/main.md" |
grep -A20 '^<a href="/?post' |
grep -E ^[ぁ-んァ-ン亜-熙　-】a-zA-Z0-9\<]  | 
grep -Ev "^(Keywords: |Copyright:|<blo)" | 
sed -e "/\<a href/a \  " -e "/\<a href/i  \ \n---\n" -e "/\<a href/s/^/###### /g" |
pandoc --template="$viewdir/template.html" -f markdown_github |
sed "s;<br />$;;g" |
sed "s;<\!--PAGER-->;<center>${HTMLanchor}</br>;g"
