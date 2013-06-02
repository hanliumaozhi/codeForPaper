chrome.extension.onMessage.addListener(function(request, sender, sendResponse){
	function trim(str){
　     return str.replace(/(^\s*)|(\s*$)/g, "");
　 	}

	if(request.action == "getItem"){
		//console.log("sss");
		var sss = document.getElementsByClassName("j_feedtitle");
		//alert(sss[0]["href"]);
		var items = new Array();
		for (var i = 0; i != 30; i++ ) {
			items[i] = sss[i]["href"];
		}
		//alert(document.getElementsByClassName("aside_user_name").length);
		//alert(document.getElementsByClassName("aside_user_name")[0].value);
		var nameArr = document.getElementsByClassName("aside_user_name");
		var userName = "";
		for (var i = 0 ; i != 1; i++) {
			userName = nameArr[i].innerHTML;
		};
		items[30] = trim(userName);
		//alert(items[30]);
		sendResponse({item : items });//document.getElementsByClassName("j_feedtitle")[href][0] });	
	}
});