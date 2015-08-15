'use strict';

function queryJson(url, data, cb){
	var params = JSON.stringify(data);
	var xhr = new XMLHttpRequest();

	xhr.open('OPTIONS', url);
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

	if(cb != undefined){
		xhr.onreadystatechange = function(){
			if(xhr.readyState == xhr.DONE){
				cb(JSON.parse(xhr.responseText));
			}
		}
	}

	xhr.send(params);

	return xhr;
}

