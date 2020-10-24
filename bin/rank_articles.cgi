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
head -n "$num"              |
while read pv d ; do
    sed "s;</a>;($pv views)&<br />;" "$datadir/$d/link"
done |
sed '1iContent-Type: text/html\n\n<h2>PV Ranking</h2>'
