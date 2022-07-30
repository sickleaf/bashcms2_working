#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2>> "$logdir/$(date +%Y%m%d).$(basename $0)"
set -o pipefail

trap 'rm -f $tmp-*' EXIT

source "$appdir/bashcmsFunc.cgi"

### VARIABLES ###
tmp=/tmp/$$
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')"
[ -z "$dir" ] && dir="pages/top"
[ "$dir" = "post" ] && dir="$(tail -n 1 "$datadir/post_list" | cut -d' ' -f 3)"

## get articleList. filter .md OR .txt, sorted in latest order, $1=timestamp,$2=fullpath
find "${contentsdir}/${dir}" -type f -printf "%A+ %p\n" | grep -E "\.(txt|md)$" | sort -k1,1r  > $tmp-articleList

# if $tmp-articleList contains no line,QUIT with 503.
[ -s "$tmp-articleList" ] || { echo "${contentsdir}/${dir} contains no textfile. check directory or querystring."; exit 503; }

# check main.md exists
if [ ! "$(grep "main.md$" $tmp-articleList)" = "" ]; then
	# if exists, make page with pandoc
	md="$contentsdir/$dir/main.md"
else
	# if doesn't exist, show plain text(.txt/.md). then,quit.
	md=$(head -1 $tmp-articleList | cut -d" " -f2)

        pandoc --template="$viewdir/plainTemplate.html" $md
	return
fi

### MAKE MATADATA ###
counter="$datadir/counters/$(tr '/' '_' <<< $dir)"
[ ! -f $counter ] && touch $counter
echo -n 1 >> "$counter" # increment the counter

cat << FIN > $tmp-meta.yaml
---
created_time: '$(cat "$datadir/$dir/created_time")'
modified_time: '$(cat "$datadir/$dir/modified_time")'
title: '$(cat "$datadir/$dir/title")'
navPrev: '$(cat "$datadir/$dir/nav" | sed "s;</a> 次の記事:.*;</a>;g" )'
navNext: '$(cat "$datadir/$dir/nav" | grep -o "次の記事.*</a>" )'
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
	preCheck "$md" |
	pandoc --toc --toc-depth=3 --template="$viewdir/template.html"	\
	    -f markdown_github+yaml_metadata_block - "$tmp-meta.yaml"  |
	sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;" |
	sed "s;/$dir/#;#;g" |
	sed 's;href="<a href="\(.*\)"[^>]*>.*</a>";href="\1";'

fi
