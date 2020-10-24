#!/bin/bash
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

[ ! -v articleNum ] && articleNum=10

ls -lU "$datadir/counters"  |
tail -n +2                  | 
awk '{print $5,$NF}'        |
awk 'NF>=2'                 |
sed 's;_;/;'                |
sort -s -k1,1nr             |
head -n "$((articleNum+1))"		|
awk '$0=$2'		|
sed 1d 			|
nl			|
while read rankNo d ; do
	if [ $rankNo -le 10 ]; then
		sed "s;</a>;&<br />;" "$datadir/$d/link" | sed "s;<a;<strong>${rankNo}</strong> &;g"
	else
		sed "s;</a>;&<br />;" "$datadir/$d/link" | sed "s;<a;${rankNo} &;g"
	fi;
done |
sed '1iContent-Type: text/html\n\n<h2>PV Ranking</h2>'
