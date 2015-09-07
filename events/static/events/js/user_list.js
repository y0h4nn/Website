'use strict';

function update_list(data){
    if(data['status'] === 1){
        this.parentNode.parentNode.removeChild(this.parentNode);
    }
}

function del_ins(iid, ext, elmt){
    if(ext){
        queryJson('', {"iid": iid, 'ext': true}, update_list.bind(elmt));
    }
    else{
        queryJson('', {"iid": iid}, update_list.bind(elmt));
    }
}
