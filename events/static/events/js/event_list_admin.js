'use strict'

function update_list(data){
	if(data['status'] === 1){
		this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
	}
}

function del_event(eid, elmt){
	queryJson('', {"eid": eid}, update_list.bind(elmt));
}
