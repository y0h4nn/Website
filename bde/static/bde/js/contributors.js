"use strict";


var title = "Choisissez le moyen de paiement.";
var choices = {
    'cash': 'Espèces',
    'card': 'Carte de crédit',
    'check': 'Chèque',
};


function onUserBuildCallback(user){

    var info = function(){
        var popup = new RemoteHtmlPopup('/bde/contributors/' + user.id);
        popup.pop();
    };

    var halfContribution = function(){
        if(this.isToggled()){
            queryJson('', {'user': user.id, 'action': 'half_contribution_delete'}, function(resp){
                if(resp.error){
                    alert(resp.error);
                }
                else{
                    this.setUntoggled();
                }
            }.bind(this));
        }
        else{
            var selector = new SelectionPopup(title, choices, function(choice){
                queryJson('', {'user': user.id, 'action': 'half_contribution_add', 'mean': choice}, function(resp){
                    if(resp.error){
                        alert(resp.error);
                    }
                    else{
                        this.setToggled();
                        this.element.nextSibling.setAttribute('class', '');
                    }
                }.bind(this));
            }.bind(this));
            selector.pop();
        }
    };

    var fullContribution = function(){
        if(this.isToggled()){
            queryJson('', {'user': user.id, 'action': 'full_contribution_delete'}, function(resp){
                if(resp.error){
                    alert(resp.error);
                }
                else{
                    this.setUntoggled();
                }
            }.bind(this));
        }
        else{
            var selector = new SelectionPopup(title, choices, function(choice){
                queryJson('', {'user': user.id, 'action': 'full_contribution_add', 'mean': choice}, function(resp){
                    if(resp.error){
                        alert(resp.error);
                        this.setUntoggled();
                    }
                    else{
                        this.setToggled();
                        this.element.previousSibling.setAttribute('class', '');
                    }
                }.bind(this));
            }.bind(this));
            selector.pop();
        }
    };

    var btnHalfContToggled = false;
    var btnFullContToggled = false;

    if(user.contribution){
        if(user.contribution == 'half') btnHalfContToggled = true;
        if(user.contribution == 'full') btnFullContToggled = true;
    }

    return [
        new UserList.UserAction('Détails', info),
        new UserList.UserAction('Demi cotiz', halfContribution, btnHalfContToggled),
        new UserList.UserAction('Full cotiz', fullContribution, btnFullContToggled),
    ];
}


window.addEventListener('load', function(){
    var userList = new UserList('userlist', onUserBuildCallback);
});
