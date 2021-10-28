#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

word=$(nkf --url-input <<< ${QUERY_STRING} | sed 's/^key=//')

#tac "$datadir/keyword_list"     |
#grep -F ",$word,"               |
#awk '{print $1}'                |
#xargs -I@ cat "$datadir/@/link" |
#sed 's/^/* /'                   |
#sed "1i# Keyword: $word"        |
#pandoc --template="$viewdir/template.html"

tac "$datadir/keyword_list"     |
grep -F ",$word,"               |
awk '{print $1}'                |
xargs -I@ cat "$datadir/@/link_date" "$contentsdir/@/main.md" |
grep -A15 '^<a href="/?post' |
grep -E ^[ぁ-んァ-ン亜-熙　-】a-zA-Z0-9\<]  | 
grep -Ev "^(Keywords: |articleTitle: |Copyright:|<blo)" |
sed -e "/\<a href/a \  " -e "/\<a href/i  \ \n---\n" -e "/\<a href/s/^/###### /g" -e "1i# Keyword: \"$word\"" |
pandoc --template="$viewdir/template.html"
