'use strict';

(function(){

    var UserList = function(containerId, listProvider, buildCallback){
        BaseList.call(this, containerId, buildCallback);
        queryJson(listProvider, {}, this.populate.bind(this));
    };

    UserList.prototype = Object.create(BaseList.prototype, {
        populate: {
            value: function(json){
                this.elems = json['users'];
                for(var user of this.elems){
                    var img = document.createElement('img');
                        img.setAttribute('src', user['picture']);
                        img.setAttribute('alt', 'profile_picture');
                    var pictureContainer = document.createElement('div');
                        pictureContainer.setAttribute('class', 'picture_container');
                    var nameContainer = document.createElement('div');
                        nameContainer.innerHTML = user['display_name'];
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    user.element = document.createElement('li');
                    user.element.appendChild(pictureContainer);
                    user.element.appendChild(nameContainer);
                    user.element.appendChild(actionContainer);
                    if(this.onElemBuild){
                        for(var action of this.onElemBuild(user)){
                            actionContainer.appendChild(action.element);
                        }
                    }
                    pictureContainer.appendChild(img);
                    this.listelement.appendChild(user.element);
                }

                this.matchingElems = this.elems;
                this.matchingElems.sort(function(a, b){
                    var nameA = a['display_name'].toLowerCase();
                    var nameB = b['display_name'].toLowerCase();

                    if(nameA > nameB) return 1;
                    else if(nameA < nameB) return -1;
                    else return 0;
                });

                this.render();
            },
        },

        match: {
            value: function(user){
                var match = false;
                var regex = this.cachedSearchRegex;
                match |= regex.test(user['last_name']);
                match |= regex.test(user['first_name']);
                match |= regex.test(user['nickname']);
                match |= regex.test(user['username']);
                match |= regex.test(user['display_name']);
                return match;
            },
        },
    });

    window.UserList = UserList;
    window.UserList.UserAction = Action;

})();
