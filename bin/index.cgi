#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
set -o pipefail

trap 'rm -f $tmp-*' EXIT

source "$appdir/bashcmsFunc.cgi"

### VARIABLES ###
tmp=/tmp/$$
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')"
[ -z "$dir" ] && dir="pages/top"
[ "$dir" = "post" ] && dir="$(tail -n 1 "$datadir/post_list" | cut -d' ' -f 3)"
md="$contentsdir/$dir/main.md"
[ -f "$md" ]

### MAKE MATADATA ###
counter="$datadir/counters/$(tr '/' '_' <<< $dir)"
[ ! -f $counter ] && touch $counter
echo -n 1 >> "$counter" # increment the counter

cat << FIN > $tmp-meta.yaml
---
created_time: '$(cat "$datadir/$dir/created_time")'
modified_time: '$(cat "$datadir/$dir/modified_time")'
title: '$(cat "$datadir/$dir/title")'
nav: '$(cat "$datadir/$dir/nav")'
views: '$(ls -l "$counter" | cut -d' ' -f 5)'
ogpmd: '$(cat "$md" | grep -vE "[!$&'()*+,-./:;<=>?@\`\[\\^_{|}~]"  | sed "s;#* ;;g" | tr "\n" " " | iconv -f utf8 -t sjis | cut -c 1-160 | iconv -c -f sjis -t utf8)'
$(cat "$contentsdir/config.yaml" )
---
FIN

if [ "${dir}" = "pages/top" ]; then

	### OUTPUT ###
	start=1
	end=${articleNum}

	articleListNum=$(grep -c ^ "$datadir/post_list")

	HTMLanchor="$(pageAnchorHTML ${articleListNum} 1 ${articleNum})"

	tac "$datadir/post_list"	|
	sed -n "${start},${end}p"	|
	awk '{print $3}'		> $tmp-viewlist

	viewlistHTML "$tmp-viewlist" "$HTMLanchor"

else

	### OUTPUT ###
	pandoc --toc --toc-depth=3 --template="$viewdir/template.html"	\
	    -f markdown_github+yaml_metadata_block "$md" "$tmp-meta.yaml"  |
	sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;" |
	sed "s;/$dir/#;#;g" |
	sed 's;href="<a href="\(.*\)"[^>]*>.*</a>";href="\1";'

fi
