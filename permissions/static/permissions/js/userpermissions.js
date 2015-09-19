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

    queryJson('', {'uid': user.id, 'action': 'list'}, this.fillContent.bind(this));
}

UserPermissionPopup.prototype = Object.create(Popup.prototype, {

    fillContent: {
        value: function(json){

            console.log(json['perms'].length);
            console.log(json['perms']);
            for(var name  in json['perms']){
                var section = this.getOrCreateSection(name);
                for(var i in json['perms'][name]){
                    var perm = json['perms'][name][i];
                    section.addPerm(perm.name, perm.codename, perm.state, this.user);
                }
            }

            this.spinner.setAttribute('class', 'hidden');
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
