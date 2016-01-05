'use strict';

function update_button(data){
    var cur_nb = parseInt(this.parentNode.getElementsByClassName("inscription_count")[0].childNodes[1].innerHTML);
    if(data['registered'] === 1){
        this.innerHTML = "Se désinscrire";
        this.className = "red_button";
        cur_nb += 1;
    }
    else{
        this.className = "";
        this.innerHTML = "S'inscrire";
        if(!data['full']){
            cur_nb -= 1;
        }
        else{
            add_message('warning', "Il ne reste plus de place à cet évènement")
        }
    }
    this.parentNode.getElementsByClassName("inscription_count")[0].childNodes[1].innerHTML = cur_nb;
}

function inscription(elmt, eid, formulas){
    if(elmt.className == "red_button" || !Object.keys(formulas).length){
        queryJson('', {"eid": eid}, update_button.bind(elmt));
    }
    else{
        new SelectionPopup('Choisissez une formule', formulas, function(choice){
            queryJson('', {'eid': eid, 'formula': choice}, function(resp){
                if(resp['error']){
                    add_message('error', resp['error']);
                }
                update_button.bind(elmt)(resp);
            });
        }).pop()

    }
}

