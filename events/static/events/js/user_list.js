'use strict';

function update_list(data){
    if(data['status'] === 1){
        this.parentNode.parentNode.removeChild(this.parentNode);
    }
}

function del_ins(iid, type, elmt){
        params = {"iid": iid};
        params[type] = true;
        queryJson('', params, update_list.bind(elmt));
}
