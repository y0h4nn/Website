'use strict';

function update_button(data){
	if(data['registered'] === 1){
		this.innerHTML = "Se désinscrire";
		this.className = "red_button";
	}
	else{
		this.className = "";
		this.innerHTML = "S'inscrire";
	}
}

function inscription(elmt, eid){
	queryJson('', {"eid": eid}, update_button.bind(elmt));
}

