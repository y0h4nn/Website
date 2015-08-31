

var payment_means = {
    'cash': 'Liquide',
    'card': 'Carte de crédit',
    'check': 'Chèque',
}

function sell(pid){
    new UserSelectionPopup('Choisissez un utilisateur', function(uid){
        new SelectionPopup('Chosissez un moyen de paiement', payment_means, function(choice){
            queryJson('', {'pid': pid, 'uid': uid, 'payment_mean': choice}, function(resp){
            });
        }).pop()
    }).pop()
}
