'use strict';


(function(){

    var UserListWaf = function(containerId, listProvider, buildCallback){
        BaseList.call(this, containerId, buildCallback);
        this.searchInput.id = "search_input";
        queryJson(listProvider, {}, this.populate.bind(this));
    };

    UserListWaf.prototype = Object.create(BaseList.prototype, {
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
                        nameContainer.appendChild(document.createTextNode(user['display_name']));
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    user.element = document.createElement('li');
                    user.klass = user['color'];
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
                    user.element.addEventListener("click", (function(list){
                        document.popup = new RemoteHtmlPopup("Info", event_id + "/info/" + this['type'] + '/' + this['id']);
                        document.popup.element = this.element;
                        document.popup.user = this;
                        document.popup.pop();
                        document.popup.onClose = function(){
                            list.updateElems();
                            list.render();
                        }
                    }).bind(user, this));
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

    window.UserListWaf = UserListWaf;
    window.UserListWaf.UserAction = Action;

})();

(function(){

    var payment_means = {
        'cash': 'Liquide',
        'card': 'Carte de crédit',
        'check': 'Chèque',
    };

    var UserListNL = function(containerId, listProvider, buildCallback){
        BaseList.call(this, containerId, buildCallback);
        this.searchInput.id = "search_input";
        queryJson(listProvider, {}, this.populate.bind(this));
    };

    UserListNL.prototype = Object.create(BaseList.prototype, {
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
                        nameContainer.appendChild(document.createTextNode(user['display_name']));
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    user.element = document.createElement('li');
                    user.klass = user['color'];
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
                        if(this.klass == "" || this.klass == "bg-red"){  // He needs to pay.
                            document.popup = new SelectionPopup(this.display_name, payment_means, function(choice){
                                queryJson('nl_ack', {'type': this.user.type, 'eid': event_id, 'iid': this.user.id, 'user': this.user.user, 'payment_mean': choice}, function(resp){
                                    if(resp['error']){
                                        add_message('error', resp['error']);
                                    }
                                    else{
                                        document.popup.element.setAttribute("class", "bg-blue");
                                        document.popup.user.klass = "bg-blue";
                                        var input =  document.getElementById('search_input');
                                        input.value = "";
                                        input.focus();
                                        acked({"status": 1})
                                    }
                                });
                            });
                            document.popup.element = this.element;
                            document.popup.user = this;
                            document.popup.pop();
                        }
                        else if(this.klass == "bg-green"){  // Contributor
                            document.popup = new RemoteHtmlPopup(this.display_name, event_id + "/nl_ack_popup/" + this['id']);
                            document.popup.element = this.element;
                            document.popup.user = this;
                            document.popup.pop();
                        }
                        else{  // Already in.
                            document.popup = new RemoteHtmlPopup("Info", event_id + "/nl_info/" + this['type'] + '/' + this['id']);
                            document.popup.element = this.element;
                            document.popup.user = this;
                            document.popup.pop();
                        }
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

    window.UserListNL = UserListNL;
    window.UserListNL.UserAction = Action;

})();
