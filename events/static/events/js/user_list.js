'use strict';

function update_list(data){
	if(data['status'] === 1){
		this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
	}
}

function del_user(eid, uid, elmt){
	queryJson('', {"uid": uid, "eid": eid}, update_list.bind(elmt));
}
