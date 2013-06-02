function getTopicAdress(topicUrl){
	var re = /[0-9]+/;
	return topicUrl.match(re)[0];
}

setTimeout(
function work(){
	var userIDArr = "";
	var topicIDArr = new Array();
	chrome.tabs.query({url : 'http://tieba.baidu.com/i/*'}, function (tab) {
		userIDArr = getTopicAdress(tab[0].url);
		chrome.tabs.sendMessage(tab[0].id, {action: "getItem"}, function(response) {
	 		if(response.item){
	 			count = 0;
				for (var i = 0; i != 30; i++) {
	 				document.writeln(getTopicAdress(response.item[i]));
	 				topicIDArr[count] = getTopicAdress(response.item[i]);
	 				count++;
	 			};
	 			document.writeln("用户ID")
	 			document.writeln(response.item[30])
	 			var topicIdToPost="";
				document.writeln(topicIDArr.length);
				topicIdToPost += response.item[30];
				topicIdToPost += "##";
				for (var i = 0; i != 30; i++) {
					topicIdToPost += topicIDArr[i];
					topicIdToPost += "##";
				};
				$.ajax({
					type: "POST",
					url: "http://127.0.0.1:8000",
					data : {
						"userID" : userIDArr,
						"topicId" : topicIdToPost
					} ,
					dataType: 'json',
					success: function(msg){
						chrome.tabs.create({"url":("http://127.0.0.1:8000/han/" + msg['userID'] + "/")});
					},
        			error : function(msg){
						document.writeln("error");
					}
				});
	 		}
    	});
	});
},500);

chrome.browserAction.onCliced.addListener(work);

