var payment_means = {
    'cash': 'Liquide',
    'card': 'Carte de crédit',
    'check': 'Chèque',
}

function sell_product(pid){
    new UserSelectionPopup('Choisissez un utilisateur', function(uid){
        new SelectionPopup('Chosissez un moyen de paiement', payment_means, function(choice){
            queryJson('', {'pid': pid, 'uid': uid, 'payment_mean': choice, 'type': 'product'}, function(resp){
            });
        }).pop()
    }).pop()
}

function sell_pack(pid){
    new UserSelectionPopup('Choisissez un utilisateur', function(uid){
        new SelectionPopup('Chosissez un moyen de paiement', payment_means, function(choice){
            queryJson('', {'pid': pid, 'uid': uid, 'payment_mean': choice, 'type': 'pack'}, function(resp){
            });
        }).pop()
    }).pop()
}
