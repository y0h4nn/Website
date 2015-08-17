'use strict';

(function(){

    var UserList = function(containerId){
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

        this.populateUsers = function(json){
            this.users = json['users'];
            for(var user of this.users){
                var link = document.createElement('a');
                    link.setAttribute('href', user['profile_url']);
                var img = document.createElement('img');
                    img.setAttribute('src', user['picture']);
                    img.setAttribute('alt', 'profile_picture');
                var pictureContainer = document.createElement('div');
                    pictureContainer.setAttribute('class', 'picture_container');
                var nameContainer = document.createElement('div');
                    nameContainer.innerHTML = user['display_name'];

                user['element'] = document.createElement('li');
                user['element'].appendChild(link);
                link.appendChild(pictureContainer);
                link.appendChild(nameContainer);
                pictureContainer.appendChild(img);
            }

            this.matchingUsers = this.users;
            this.matchingUsers.sort(function(a, b){
                var nameA = a['display_name'].toLowerCase();
                var nameB = b['display_name'].toLowerCase();

                if(nameA > nameB) return 1;
                else if(nameA < nameB) return -1;
                else return 0;
            });

            for(var user of this.users){
                this.listelement.appendChild(user.element);
            }

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
                    user.element.setAttribute('class', '');
                }
                else{
                    user.element.setAttribute('class', 'hidden');
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

})();
