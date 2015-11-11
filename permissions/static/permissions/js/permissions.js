"user strict";

/*
 * Base Permssion class
 */

function Permission(name, codename, state, enabled){
    this.name = name;
    this.codename = codename;

    this.element = document.createElement('div');
    this.checkbox = document.createElement('input');
    this.checkbox.setAttribute('type', 'checkbox');
    this.checkbox.setAttribute('id', codename);
    this.checkbox.checked = state;
    if(!enabled){
        this.checkbox.setAttribute('disabled', true);
    }
    this.label = document.createElement('label');
    this.label.setAttribute('for', codename);
    this.label.appendChild(document.createTextNode(name));
    this.element.appendChild(this.checkbox);
    this.element.appendChild(this.label);

    this.checkbox.addEventListener('change', this.onchange.bind(this));
}

Permission.prototype = {
    appendTo: function(element){
        element.appendChild(this.element);
    },
    onchange: function(){
    },
};

/*
 * XXX
 * As the sole difference between UserPermission and GroupPermission below, it may be possible
 * to only use permission by providing group and user as unknow object to Permission
 */

/*
 * User permission
 */

function UserPermission(name, codename, state, enabled, user){
    Permission.call(this, name, codename, state, enabled);
    this.user = user;
}


UserPermission.prototype = Object.create(Permission.prototype, {
    onchange: {
        value: function(){
            queryJson('', {
                'uid': this.user.id,
                'action': 'set_perm',
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
 * Group permissions
 */

function GroupPermission(name, codename, state, enabled, group){
    Permission.call(this, name, codename, state, enabled);
    this.group = group;
}

GroupPermission.prototype = Object.create(Permission.prototype, {
    onchange: {
        value: function(){
            queryJson('', {
                'gid': this.group.id,
                'action': 'set_perm',
                'codename': this.codename,
                'state': this.checkbox.checked,
            }, function(){
                // callback
            });
        },
    },
});

GroupPermission.prototype.constructor = UserPermission;

/*
 * Permission Section
 */

function PermSection(name, permCls){
    this.name = name;
    this.permCls = permCls;
    this.element = document.createElement('div');
    this.title = document.createElement('h4');
    this.title.innerHTML = name;

    this.element.appendChild(this.title);
    this.perms = [];
};

PermSection.prototype = {
    appendTo: function(element){
        element.appendChild(this.element);
    },

    addPerm: function(perm, user){
        permObj = new this.permCls(perm.name, perm.codename, perm.state, perm.enabled, user);
        permObj.appendTo(this.element);
        this.perms.push(permObj);
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
            for(var i in this.sections){
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
    this.groupContainer = document.createElement('div');
    this.groupTitle = document.createElement('h4');
    this.groupTitle.innerHTML = "Certaines permissions sont hérités des groupes suivants";
    this.groupList = document.createElement('ul');
    this.groupList.id = 'grouplist'
    this.groupContainer.appendChild(this.groupTitle);
    this.groupContainer.appendChild(this.groupList);
    this.main.appendChild(this.groupContainer);

    queryJson('', {'uid': user.id, 'action': 'list_perms'}, this.fillContent.bind(this));
}

UserPermissionPopup.prototype = Object.create(PermissionPopup.prototype, {
    permissionClass: {
        value: UserPermission
    },
    fillContent: {
        value: function(json){
            this.clear();
            for(var i in json['groups']){
                var group = json['groups'][i];
                var li = document.createElement('li');
                li.appendChild(document.createTextNode(group.name));

                var sum = 0;
                for(var i = 0; i < 3; i++){
                    sum += parseInt(group.color.slice(i + 1, i + 3), 16);
                }
                var avg = sum/3;

                if(avg >= 0x7F){
                    var textColor = "#000000";
                }
                else{
                    var textColor = "#FFFFFF";
                }
                li.setAttribute('style', 'background-color: ' + group.color + '; color: ' + textColor);
                this.groupList.appendChild(li);
            }
            for(var i in json['perms']){
                var perm = json['perms'][i];
                var section = this.getOrCreateSection(perm.section);
                section.addPerm(perm, this.user);
            }
            this.spinner.setAttribute('class', 'hidden');
        },
    },

});

UserPermissionPopup.prototype.constructor = UserSelectionPopup;


/*
 * Group permissions popup
 */
function GroupPermissionPopup(title, group){
    PermissionPopup.call(this, title);
    this.group = group;
    queryJson('', {'gid': this.group.id, 'action': 'list_perms'}, this.fillContent.bind(this));
}

GroupPermissionPopup.prototype = Object.create(PermissionPopup.prototype, {
    permissionClass: {
        value: GroupPermission,
    },

    fillContent: {
        value: function(json){
            this.clear();
            for(var i in json['perms']){
                var perm = json['perms'][i];
                var section = this.getOrCreateSection(perm.section);
                section.addPerm(perm, this.group);
            }
            this.spinner.setAttribute('class', 'hidden');
        },
    },
});

GroupPermissionPopup.prototype.constructor = GroupPermissionPopup;
