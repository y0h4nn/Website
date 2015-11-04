"user strict";

/*
 * Base Permssion class
 */

function Permission(name, codename, state){
    this.name = name;
    this.codename = codename;

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

    this.checkbox.addEventListener('change', this.onchange.bind(this));
}

Permission.prototype = {
    appendTo: function(element){
        element.appendChild(this.element);
    },
    onchange: function(){
        console.log(this);
        console.log("NOP");
    },
};


/*
 * User permission
 */

function UserPermission(name, codename, state, user){
    Permission.call(this, name, codename, state);
    this.user = user;
}


UserPermission.prototype = Object.create(Permission.prototype, {
    onchange: {
        value: function(){
            queryJson('', {
                'uid': this.user.id,
                'action': 'set',
                'codename': this.codename,
                'state': this.checkbox.checked,
            }, function(){
                // callback
            });
        },
    },
});

UserPermission.prototype.constructor = UserPermission;

/*
 * Permission Section
 */

function PermSection(name, permCls){
    this.name = name;
    this.permCls = permCls;
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
        perm = new this.permCls(name, codename, state, user);
        perm.appendTo(this.element);
        this.perms.push(perm);
    },

    clear: function(){
        this.element.parentNode.removeChild(this.element);
    },


};


/*
 * PermissionPopup
 */

function PermissionPopup(title){
    Popup.call(this, title);
    this.baseClass = 'permission_popup';
    this.sections = [];
    this.spinner = document.createElement('div');
    this.spinner.setAttribute('class', 'spinner');
    this.main.appendChild(this.spinner);
}

PermissionPopup.prototype = Object.create(Popup.prototype, {
    permissionClass: {
        value: Permission
    },

    clear: {
        value: function(){
            for(var i in this.sections){
                this.sections[i].clear();
            }
            this.sections = [];
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
            var section = new PermSection(name, this.permissionClass);
            section.appendTo(this.main);
            this.sections.push(section);
            return section;
        },
    },
});

Permission.prototype.constructor = PermissionPopup;

/*
 * UserPermissionPopup
 */


function UserPermissionPopup(title, user){
    PermissionPopup.call(this, title);
    this.user = user;

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

UserPermissionPopup.prototype = Object.create(PermissionPopup.prototype, {
    permissionClass: {
        value: UserPermission
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
});

UserPermissionPopup.prototype.constructor = UserSelectionPopup;
