'use strict';

function update_list(data){
    if(data['status'] === 1){
        this.parentNode.parentNode.removeChild(this.parentNode);
    }
}

function del_ins(iid, type, elmt){
        queryJson('', {"iid": iid, type: true}, update_list.bind(elmt));
}
