#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

tac "$datadir/keyword_list"                                                         |
grep -oE ",.+,"                                                                     |
cut -d"," -f2-                                                                      |
sed -e "s/,$//g" -e "s/,/\n/g"					                    |
sort                                                                                |
uniq -c                                                                             |
sort -k2,2                                                                          |
awk -v size=5 -v keynum=$(grep -c ^ "$datadir/keyword_list") ' \
	{if(keynum*0.1<$1)size=4; \
	 if(keynum*0.2<$1)size=3; \
	 if(keynum*0.35<$1)size=2; \
	 if(keynum*0.5<$1)size=1;  \
	 print size,$0;\
	 size="6"}' |
awk '{print "@" $1 "@<a href=\"/key.cgi?key=" $3 "\">" $3  "(" $2 ")</a></span>" }' |
sed "s;@\(.\)@;<span class=\"h\1\">;g"                                              |
sed '1iContent-Type: text/html\n\n<h2>Tag Cloud</h2>'
