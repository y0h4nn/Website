'use strict';

(function(){

    var UserAction = function(name, callback, toggled){
        this.callback = callback;
        this.element = document.createElement('button');
        this.element.setAttribute('type', 'button');
        this.element.innerHTML = name;

        this.element.addEventListener('click', function(event){
            this.callback(event);
        }.bind(this));

        this.setToggled = function(){
            this.element.setAttribute('class', 'toggled');
        };

        this.setUntoggled = function(){
            this.element.setAttribute('class', '');
        };

        this.toggle = function(){
            if(this.element.getAttribute('class') == 'toggled'){
                this.setUntoggled();
            }
            else{
                this.setToggled();
            }
        };

        this.isToggled = function(){
            if(this.element.getAttribute('class') == 'toggled'){
                return true;
            }
            else{
                return false;
            }
        };

        if(toggled){
            this.setToggled();
        }
    }

    var UserList = function(containerId, buildCallback, clickCallback){
        this.element = document.getElementById(containerId);
        this.searchInput = document.createElement('input');
        this.spinner = document.createElement('div');
        this.spinner.setAttribute('class', 'spinner');
        this.listelement = document.createElement('ul');
        this.listelement.setAttribute('class', 'userlist');
        this.users = []
        this.matchingUsers = []
        this.cachedSearchRegex = new RegExp('');
        this.element.appendChild(this.searchInput);
        this.element.appendChild(this.spinner);
        this.element.appendChild(this.listelement);

        // hooks
        this.onUserBuild = buildCallback;
        this.onClick = clickCallback;

        this.populateUsers = function(json){
            this.users = json['users'];
            for(var user of this.users){
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
                if(this.onUserBuild){
                    for(var action of this.onUserBuild(user)){
                        actionContainer.appendChild(action.element);
                    }
                }
                pictureContainer.appendChild(img);
                this.listelement.appendChild(user.element);
            }

            this.matchingUsers = this.users;
            this.matchingUsers.sort(function(a, b){
                var nameA = a['display_name'].toLowerCase();
                var nameB = b['display_name'].toLowerCase();

                if(nameA > nameB) return 1;
                else if(nameA < nameB) return -1;
                else return 0;
            });


            this.render();
        };

        this.match = function(user){
            var match = false;
            var regex = this.cachedSearchRegex;
            match |= regex.test(user['last_name']);
            match |= regex.test(user['first_name']);
            match |= regex.test(user['nickname']);
            match |= regex.test(user['username']);
            match |= regex.test(user['display_name']);
            return match;
        }

        this.render = function(){
            this.spinner.setAttribute('class', 'spinner hidden');

            for(var user of this.users){
                if(this.matchingUsers.indexOf(user) >= 0){
                    user.element.className = '';
                }
                else{
                    user.element.className = 'hidden';
                }
            }
        };

        queryJson('/accounts/members/', {}, this.populateUsers.bind(this));

        this.searchInput.addEventListener('keyup', function(){
            if(this.timer){
                clearTimeout(this.timer);
            }
            this.timer = setTimeout(function(){
                var startDate = new Date();

                var pattern = this.searchInput.value.split('').join('.*?');
                this.cachedSearchRegex = new RegExp(pattern, 'i');

                this.matchingUsers = this.users.filter(this.match, this);
                this.render();
                console.log("Search update and rendering in " + (new Date() - startDate + "ms"));
            }.bind(this), 100);
        }.bind(this));
    }

    window.UserList = UserList;
    window.UserList.UserAction = UserAction;

})();
