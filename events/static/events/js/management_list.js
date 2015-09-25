'use strict';

(function(){

    var UserList = function(containerId, listProvider, buildCallback){
        BaseList.call(this, containerId, buildCallback);
        queryJson(listProvider, {}, this.populate.bind(this));
    };

    UserList.prototype = Object.create(BaseList.prototype, {
        populate: {
            value: function(json){
                // Registrations
                this.elems = json['reg'].concat(json['ext_reg']).concat(json['invits']);

                for(var i in this.elems){
                    var user = this.elems[i];
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
                    if(user['contributor'] === true){
                        user.klass = "bg-green";
                    }
                    else if(user['contributor'] === false){
                        user.klass = "bg-red";
                    }
                    user.element.appendChild(pictureContainer);
                    user.element.appendChild(nameContainer);
                    user.element.appendChild(actionContainer);
                    if(this.onElemBuild){
                        var actions = this.onElemBuild(user);
                        for(var i in actions){
                            actionContainer.appendChild(actions[i].element);
                        }
                    }
                    pictureContainer.appendChild(img);
                    user.element.addEventListener("click", (function(){
                        document.popup = new RemoteHtmlPopup("Info", event_id + "/info/" + this['type'] + '/' + this['id']);
                        document.popup.pop();
                    }).bind(user));
                    this.listelement.appendChild(user.element);
                }

                this.matchingElems = this.elems;
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

