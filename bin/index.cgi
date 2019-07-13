#!/bin/bash -euvx

source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

### VARIABLES ###
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;' )"
md="$contentsdir/$dir/main.md"

[ -f "$md" ]

### MAKE HTML ###
pandoc --template="$viewdir/template.html" -f markdown_github+yaml_metadata_block "$md" |
sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;"	|
sed "s;/$dir/#;#;g"
