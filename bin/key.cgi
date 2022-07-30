#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2>> "$logdir/$(date +%Y%m%d).$(basename $0)"

trap 'rm -f $tmp-*' EXIT
source "$appdir/bashcmsFunc.cgi"

tmp=/tmp/$$
word=$(nkf --url-input <<< ${QUERY_STRING} | sed 's/^key=//')

tac "$datadir/keyword_list"     |
grep -F ",$word,"               |
awk '{print $1}'                > $tmp-kwdlist

viewlistHTML "$tmp-kwdlist" ""
