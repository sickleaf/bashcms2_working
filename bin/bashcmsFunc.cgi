# get ${pageNum}'th anchor , when all post numbers are ${articleListNum}
function pageAnchorHTML() {

	articleListNum=$1
		
	pageNum=$2

	articleNum=$3
	
	
	topParts="＜＜　　"
	nextParts="＜　　"
	prevParts="　　＞"
	lastParts="　　＞＞"
	
	topLink=""
	nextLink=""
	prevLink=""
	lastLink=""
	
	htmlParts=""
	
	# articleListNum is less equal pageNum ; only one page AND  no link for anchor
	[ ${articleListNum} -le ${pageNum} ] && { echo " <  1 / 1  >"; return 0; }
	
	
	## <<after this line, at least two pages needed. (at least one link will be set) >>
	

	###############################
	#  remove "<<" , ">>"
	###############################

	## if num=1; remove "<<" and "<"
	[ ${pageNum} -eq 1 ] && { topParts=""; nextParts=""; }

	## if num=${endPage}; remove ">>" and ">"

	endPageDC=$(echo $articleListNum $articleNum | awk '{print $1/$2}')
	endPageInt=$(echo ${endPageDC} | cut -d. -f1 )
	dotInclude=$(echo ${endPageDC} | grep '\.' | wc -l)
	endPage=$(( endPageInt + dotInclude))

	[ ${pageNum} -eq ${endPage} ] && { lastParts=""; prevParts=""; }
	
	
	###############################
	#  set link for (top|next|prev|last)parts; according to pageNum and articleListNum)
	###############################

	if [ ${articleListNum} -gt $((pageNum*2)) ]; then	# at least three page
	
		# set link for nextParts,prevParts
		nextLink=$((pageNum-1))
		prevLink=$((pageNum+1))
		
		# if pageNum != 1, set link for topParts 
		[ -n "${topParts}" ] && topLink=1
		
		# if pageNum != endPage, set link for lastParts
		[ -n "${lastParts}" ] && lastLink=${endPage}
	
	else	# just two page
	
		if [ ${pageNum} -eq 1 ]; then
			nextLink=2	# pageNum=1
		else
			prevLink=1	# pageNum=2
		fi
	fi
	
	[ -n "${topLink}" ] && topParts="<a href=\"viewTop.cgi?num=${topLink}\" >${topParts}</a>"
	
	[ -n "${nextLink}" ] && nextParts="<a href=\"viewTop.cgi?num=${nextLink}\" >${nextParts}</a>"
	
	[ -n "${prevLink}" ] && prevParts="<a href=\"viewTop.cgi?num=${prevLink}\" >${prevParts}</a>"
	
	[ -n "${lastLink}" ] && lastParts="<a href=\"viewTop.cgi?num=${lastLink}\" >${lastParts}</a>"
	
	htmlParts="${topParts}\t${nextParts}\t${pageNum} / ${endPage}\t${prevParts}\t${lastParts}"

	echo "${htmlParts}"

}


#from pages/posts list and anchorHTML, generate HTML
function viewlistHTML() {
        viewlistPath="$1"
        HTMLanchor="$2"

        cat "${viewlistPath}" |
        xargs -I@ cat "$datadir/@/link_date" "$contentsdir/@/main.md" <(echo "") |
        sed -E "/^---[ ]*$/,/^---[ ]*$/d" |
        sed "/^\`\`\`/,/^\`\`\`/d" |
        grep -A20 '^<a href="/?post' |
        grep -E ^[ぁ-んァ-ン亜-熙　-】a-zA-Z0-9#\<]  |
        grep -Ev "^(<blo|<hr|#{3,6})" |
        uniq |
        awk ' /<a href/{print "\n---\n###### "$0} !/<a href/{print}' |
        pandoc --template="$viewdir/template.html" -f markdown_github |
        sed "s;<\!--PAGER-->;<center>${HTMLanchor}</br>;g"

}

#from pages/posts list and word, generate HTML for search result
function viewlistFullSearch() {
	viewlistPath="$1"
	word="$2"

	cat "${viewlistPath}" |
	xargs -I@ cat "$datadir/@/link_date" "$contentsdir/@/main.md" |
	sed -E "/^---[ ]*$/,/^---[ ]*$/d" |
	awk -v word=$word \
	' !(/^<a href/) && /'"$word"'/ {print "<blockquote style=\"border-left: 0.5rem solid #9ba5b9\">"$0"</blockquote>\n"} \
	  /^<a href/ {print "<hr>\n"$0"<br>\n"}' |
	sed "/^<a href/! s/$word/<strong>$word<\/strong>/g"

}

export -f pageAnchorHTML viewlistHTML viewlistFullSearch
