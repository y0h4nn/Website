"user strict";


function Permission(name, codename, state, user){
    this.name = name;
    this.codename = codename;
    this.user = user;

    this.element = document.createElement('div');
    this.checkbox = document.createElement('input');
    this.checkbox.setAttribute('type', 'checkbox');
    this.checkbox.setAttribute('id', codename);
    this.checkbox.checked = state;
    this.label = document.createElement('label');
    this.label.setAttribute('for', codename);
    this.label.innerHTML = name;
    this.element.appendChild(this.checkbox);
    this.element.appendChild(this.label);


    this.checkbox.addEventListener('change', function(){
        console.log(this.checkbox.checked);
        queryJson('', {
            'uid': user.id,
            'action': 'set',
            'codename': this.codename,
            'state': this.checkbox.checked,
        }, function(){
            // callback
        });
    }.bind(this));
}

Permission.prototype = {
    appendTo: function(element){
        element.appendChild(this.element);
    },
};


function PermSection(name){
    this.name = name;
    this.element = document.createElement('div');
    this.title = document.createElement('h3');
    this.title.innerHTML = name;

    this.element.appendChild(this.title);
    this.perms = [];

};

PermSection.prototype = {
    appendTo: function(element){
        element.appendChild(this.element);
    },

    addPerm: function(name, codename, state, user){
        perm = new Permission(name, codename, state, user);
        perm.appendTo(this.element);
        this.perms.push(perm);
    },

    clear: function(){
        this.element.parentNode.removeChild(this.element);
    },

};


function UserPermissionPopup(title, user){
    Popup.call(this, title);
    this.baseClass = 'permission_popup';
    this.sections = [];
    this.user = user;

    this.spinner = document.createElement('div');
    this.spinner.setAttribute('class', 'spinner');
    //this.spinner.setAttribute('class', 'hidden');

    this.main.appendChild(this.spinner);
    this.isSuperuserContainer = document.createElement('div');
    this.isSuperuserCheckbox = document.createElement('input');
    this.isSuperuserCheckbox.setAttribute('id', 'is_superuser');
    this.isSuperuserCheckbox.setAttribute('type', 'checkbox');
    this.isSuperuserLabel = document.createElement('label');
    this.isSuperuserLabel.innerHTML = 'Le member est super utilisateur';
    this.isSuperuserLabel.setAttribute('for', 'is_superuser');
    this.main.appendChild(this.isSuperuserContainer);
    this.isSuperuserContainer.appendChild(this.isSuperuserCheckbox);
    this.isSuperuserContainer.appendChild(this.isSuperuserLabel);



    this.isSuperuserCheckbox.addEventListener('change', function(){
        queryJson('', {'uid': user.id, 'action': 'superuser', superuser: this.isSuperuserCheckbox.checked}, this.fillContent.bind(this));
    }.bind(this));

    queryJson('', {'uid': user.id, 'action': 'list'}, this.fillContent.bind(this));
}

UserPermissionPopup.prototype = Object.create(Popup.prototype, {

    clear: {
        value: function(){
            for(var i in this.sections){
                this.sections[i].clear();
            }
            this.sections = [];
        },
    },

    fillContent: {
        value: function(json){
            this.clear();
            for(var name  in json['perms']){
                var section = this.getOrCreateSection(name);
                for(var i in json['perms'][name]){
                    var perm = json['perms'][name][i];
                    section.addPerm(perm.name, perm.codename, perm.state, this.user);
                }
            }
            this.setSuperuser(json['superuser']);
            this.spinner.setAttribute('class', 'hidden');
        },
    },

    setSuperuser: {
        value: function(superuser){
            for(var i in this.sections){
                for(var j in this.sections[i].perms){
                    // We can't simply set disabled to false to enable
                    // checkbox, attribute must be removed.
                    if(superuser){
                        this.sections[i].perms[j].checkbox.setAttribute('disabled', true);
                    }
                    else{
                        this.sections[i].perms[j].checkbox.removeAttribute('disabled');
                    }
                }
            }
            this.isSuperuserCheckbox.checked = superuser;
        },
    },

    getOrCreateSection: {
        value: function(name){
            for(var i = 0, l = this.sections.length; i < l; i++){
                if(this.sections[i].name == name){
                    return this.sections[i];
                }
            }
            return this.addSection(name);
        },
    },

    addSection: {
        value: function(name){
            var section = new PermSection(name);
            section.appendTo(this.main);
            this.sections.push(section);
            return section;
        },
    },

});

UserPermissionPopup.prototype.constructor = UserSelectionPopup;


window.addEventListener('load', function(){
    var list = new UserList('userlist', '/accounts/members/', function(user){
        function permEdit(){
            var popup = new UserPermissionPopup('Permissions de l\'utilisateur ' + user.display_name, user);
            popup.pop();

        }
        return [
            new UserList.UserAction('Editer les permissions', permEdit),
        ];
    });
});
