'use strict';

function update_button(data){
	var cur_nb = parseInt(this.parentNode.getElementsByClassName("inscription_count")[0].innerHTML);
	if(data['registered'] === 1){
		this.innerHTML = "Se désinscrire";
		this.className = "red_button";
		cur_nb += 1;
	}
	else{
		this.className = "";
		this.innerHTML = "S'inscrire";
		cur_nb -= 1;
	}
	this.parentNode.getElementsByClassName("inscription_count")[0].innerHTML = cur_nb;
}

function inscription(elmt, eid){
	queryJson('', {"eid": eid}, update_button.bind(elmt));
}

