'use strict';


function queryJson(url, data, cb){
	var params = JSON.stringify(data);
	var xhr = new XMLHttpRequest();

	xhr.open('OPTIONS', url);
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

	if(cb != undefined){
		xhr.onreadystatechange = function(){
			if(xhr.readyState == xhr.DONE){
                console.log("received datas");
                console.log(JSON.parse(xhr.responseText));
				cb(JSON.parse(xhr.responseText));
			}
		}
	}

	xhr.send(params);

	return xhr;
}


(function(){

    var UserList = function(containerId){
        this.element = document.getElementById(containerId);
        this.searchInput = document.createElement('input');
        this.listelement = document.createElement('ul');
        this.listelement.setAttribute('class', 'userlist');
        this.allUsers = []
        this.matchingUsers = []

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
            this.reset();
            this.render();
        };

        this.match = function(user){
            return new RegExp(this.searchInput.value).test(user['display_name']);
        }

        this.reset = function(){
            this.element.innerHTML = "";
            this.element.appendChild(this.searchInput);
            this.element.appendChild(this.listelement);
        };

        this.render = function(){
            this.listelement.innerHTML = "";
            for(var user of this.matchingUsers){
                this.listelement.appendChild(user['element']);
            }
        };

        queryJson('', {}, this.populateUsers.bind(this));

        this.searchInput.addEventListener('keyup', function(){
            console.log(this.searchInput.value);
            this.matchingUsers = this.users.filter(this.match, this);
            this.render();
        }.bind(this));
    }

    window.UserList = UserList;

})();
