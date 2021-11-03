#!/bin/bash -xv
source "$(dirname $0)/../conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

tmp=/tmp/$$
trap 'rm -f $tmp-*' EXIT

source "$appdir/bashcmsFunc.cgi"

word=$(nkf --url-input <<< ${QUERY_STRING} | sed 's/^word=//' )

[ "$(echo $word | tr -d "\n" | wc -c)" -gt 1 ]  || exit

numchar=$(nkf -w16B0 <<< "$word" | xxd -plain | tr -d '\n' | sed 's/..../\&#x&;/g')

cat << FIN
Content-Type: text/html

<h4>SearchResult: $numchar</h4>
FIN

tac "$datadir/all_markdown"             |
sed -E "/---[ ]/,/---[ ]/d"       |
grep -Ev "<(block|meta)"              |
grep "$word"                            |
awk '{print $1}'                        |
uniq  > $tmp-list

viewlistFullSearch "$tmp-list" "$word"
#sed "s;$word;<strong>$word</strong>;g"

