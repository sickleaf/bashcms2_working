#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

source "$(dirname $0)/bashcmsFunc.cgi"

tmp=/tmp/$$

pageNum=$(tr -dc 'a-z0-9='  <<< ${QUERY_STRING} | grep "num=" | sed "s;^num=;;g" )
ymInfo=$(tr -dc 'a-z0-9-='  <<< ${QUERY_STRING} | grep "ym=" | sed "s;^ym=;;g" )

articleListNum=$(grep -c ^ "$datadir/post_list")



if [ "x${pageNum}" = "x" ]; then
	HTMLanchor="$(pageAnchorHTML 1 1 1)"

	tac "$datadir/post_list"	|
	grep $ymInfo			|
	awk '{print $3}'		> $tmp-viewlist

else

	HTMLanchor="$(pageAnchorHTML ${articleListNum} ${pageNum} ${articleNum})"

	start=$((1+(pageNum-1)*articleNum))
	end=$((pageNum*articleNum))

	tac "$datadir/post_list"	|
	sed -n "${start},${end}p"	|
	awk '{print $3}'		> $tmp-viewlist

fi

cat $tmp-viewlist |
xargs -I@ cat "$datadir/@/link_date" "$contentsdir/@/main.md" <(echo "") |
sed "/\`\`\`/,/\`\`\`/d" |
grep -A20 '^<a href="/?post' |
grep -E ^[ぁ-んァ-ン亜-熙　-】a-zA-Z0-9\<]  | 
grep -Ev "^(Keywords: |articleTitle: |Copyright:|<blo)" |
sed -e "/\<a href/a \  " -e "/\<a href/i  \ \n---\n" -e "/\<a href/s/^/###### /g" |
pandoc --template="$viewdir/template.html" -f markdown_github |
sed "s;<br />$;;g" |
sed "s;<\!--PAGER-->;<center>${HTMLanchor}</br>;g"

rm $tmp-viewlist
