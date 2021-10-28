document.addEventListener("DOMContentLoaded", function(){
    invisibleCard();
});

window.onload = function () {
    lastArticles(5);
    rankArticles();
    tagcloud();
    monthlyArchive();
    linkKeywords();
    //fullSearch("");
}

function lastArticles(num){
    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function(){
        if(httpReq.readyState != 4 || httpReq.status != 200)
            return;

        document.getElementById("last-articles").innerHTML = httpReq.responseText;
    }
    var url = "/last_articles.cgi?num=" + num;
    httpReq.open("GET",url,true);
    httpReq.send(null);
}

function linkKeywords(){
    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function(){
        if(httpReq.readyState != 4 || httpReq.status != 200)
            return;

        document.getElementById("keywords").innerHTML = httpReq.responseText;
    }
    var word = document.getElementById("keywords").innerHTML;
    var url = "/link_keywords.cgi?keywords=" + encodeURIComponent(word);
    httpReq.open("GET",url,true);
    httpReq.send(null);
}

function fullSearch(){
    var word = document.getElementById("full-search-box").value; 
    if(word == "")
        return;

    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function(){
        if(httpReq.readyState != 4 || httpReq.status != 200)
            return;

        document.getElementById("article-body").innerHTML = httpReq.responseText;
        document.body.style.cursor = "default";
    }
    var url = "/bsview/full_search.cgi?word=" + encodeURIComponent(word);
    httpReq.open("GET",url,true);
    httpReq.send(null);
    document.body.style.cursor = "wait";
}

function rankArticles(){
    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function(){
        if(httpReq.readyState != 4 || httpReq.status != 200)
            return;

        document.getElementById("rank-articles").innerHTML = httpReq.responseText;
   }
    var url = "/rank_articles.cgi";
    httpReq.open("GET",url,true);
    httpReq.send(null);
}

function tagcloud(){
    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function(){
        if(httpReq.readyState != 4 || httpReq.status != 200)
            return;

        document.getElementById("tag-cloud").innerHTML = httpReq.responseText;
    }
    var url = "/tagcloud.cgi" 
    httpReq.open("GET",url,true);
    httpReq.send(null);
}

function invisibleCard(){
    var search = location.search;
    var pname = location.pathname;
    var key1 = new RegExp("^/key.cgi")
    var key2 = new RegExp("^/viewTop.cgi")
    if ( search === "" || key1.test(pname) || key2.test(pname) ) {
        for (let el of document.querySelectorAll("div.card")) el.style.visibility = "hidden"
    }
}

function monthlyArchive(){
    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function(){
        if(httpReq.readyState != 4 || httpReq.status != 200)
            return;

        document.getElementById("monthly-archive").innerHTML = httpReq.responseText;
    }
    var url = "/monthlyArchive.cgi"
    httpReq.open("GET",url,true);
    httpReq.send(null);
}


