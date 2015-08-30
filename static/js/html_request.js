'use strict';

function queryHtml(url, cb){
	var xhr = new XMLHttpRequest();

	xhr.open('get', url);

	if(cb != undefined){
		xhr.onreadystatechange = function(){
			if(xhr.readyState == xhr.DONE){
				cb(xhr.responseText);
			}
		}
	}

	xhr.send();
	return xhr;
}

