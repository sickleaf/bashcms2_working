#!/bin/bash -euvx
source "$(dirname $0)/conf"
source "$(dirname $0)/local/localconf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
 
echo -e 'Content-type: text/html\n'

set -o pipefail

argsErrorHead='!!  args missing. present args=${#}, needed at least ${leastArgs} (functionName=$0})\n'
argsMessage=" usage: <1:pushFlag>"
leastArgs=`echo -n ${argsMessage} | sed "s;[^*];;g" | wc -m`

[ $# -ge ${leastArgs:-0} ] || { eval "echo -e \"${argsErrorHead}${argsMessage}\" "; exit; } 


pushFlag=false
[ $# -gt 0 ] && [ -n "$1" ] && pushFlag=true

if [ -v QUERY_STRING ] &&  [ -n ${QUERY_STRING} ]; then
	word=$(nkf --url-input <<< ${QUERY_STRING} | sed 's/^push=//' )
	[ "${word}" = "true" ] &&  pushFlag=true
fi


functionScript=${myScript}/common/usefulFunction.sh
filterScript=${myScript}/common/getSpreadSheet.sh

### read function 
. ${functionScript}
. ${filterScript}

#internalPath is set in local/localconf
parsePath=${internalPath%/*}; parsePath=${parsePath}/parse
internalPath=${internalPath}-$$
parsePath=${parsePath}-$$

if [ "$(type setTrap > /dev/null 2>&1 ; echo $?)" -eq 0 ]; then
	# if estTrap defined, register trap command for each
	setTrap "rm -f ${internalPath}" EXIT
	setTrap "rm -f ${parsePath}" EXIT
	myTrap EXIT
else
	# if setTrap not defined, write trap command at once
	trap 'rm -f ${internalPath} ${parsePath}' EXIT
fi

#getSpreadSheet
getSpreadSheet ${bookID} ${sheetID} ${internalPath} tsv > /dev/null

#parse spreadsheet contents into main.md as ${parsePath}
cat ${internalPath} |
tr "\t" " " |	# due to tsv format
sed "/^Keywords:/s/ /,/g; /^Keywords:/s/,/ /; 1d" | # edit Keyword line
sed "/^ *$/s/.*/<br>/;" | # all blank line equal to <br>
sed "s/^\*\*\*/<hr>/;" | # all *** line equal to <hr>
sed "0,/<br>/ s/<br>//; \$a\ " | # delete first <br> (line 6)
awk '/\[img\] */ {print "<img src=\""$2"\" />"} /\[imgsize\] */  {print "<img src=\""$2"\" width=\""$3"\" height=\"" $4 "\" />"}  !/\[img*/{print $0}' | # [img] and [imgsize] line
awk '/\[mp4\]*/ {print "<video controls><source src=\"" $2 "\" type=\"video/mp4\"></video>"} !/\[mp4\]*/{print $0}' > ${parsePath}


# set ${articleName} from A1,A2 cell (A1:article-keyword A2:date)
titledate=$(cat ${internalPath} | sed -n 1p | awk '$0=$2' | xargs -I@ date -d "@" +"%Y%m%d")
[ "${titledate}" = "" ] && titledate=$(date +"%Y%m%d")

articleName=$(cat ${internalPath} | sed -n 1p | awk '$0=$1' | sed "s/$/_${titledate}/g")

# check header line exists
if [ $(cat ${parsePath} | grep -E "^[#]+ .+" | wc -l) -eq 0 ]; then
	echo "[[header(#)is blank ${articleName}]]"
else

	mkdir -p ${contentsdir}/posts/${articleName}

	# move ${parsePath} into main.md
	mv -v ${parsePath} ${contentsdir}/posts/${articleName}/main.md

	# if main.md exists, run GAS(${articleClearURL})
	[ $? -eq 0 ] && curl -s -G ${articleClearURL} >/dev/null

	if "${pushFlag}"; then
		echo push!
		# git add,commit,push
		cd ${contentsdir}
		git add  ${contentsdir%/}/posts/${articleName}
	
		git commit -m "[add] ${titledate} via spreadsheet"
	
		git push origin master
	
		bash ${appdir%/}/${callCGI}
		echo "https://sickleaf.work/?post=${articleName}"
	fi
fi

