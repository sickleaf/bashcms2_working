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

viewlistHTML "$tmp-viewlist" "$HTMLanchor"

rm $tmp-viewlist
