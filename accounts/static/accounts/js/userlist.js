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

        this.populateUsers = function(json){   
            this.users = json['users'];
            for(var user of this.users){
                user['element'] = document.createElement('li');
                var link = document.createElement('a');
                    link.setAttribute('href', user['profile_url']);
                var img = document.createElement('img');
                    img.setAttribute('src', user['picture']);
                    img.setAttribute('alt', 'profile_picture');
                var pictureContainer = document.createElement('div');
                    pictureContainer.setAttribute('class', 'picture_container');
                var nameContainer = document.createElement('div');
                    nameContainer.innerHTML = user['display_name'];

                user['element'].appendChild(link);
                link.appendChild(pictureContainer);
                link.appendChild(nameContainer);
                pictureContainer.appendChild(img);
            }

            this.render();
        };

        this.render = function(){
            var ul = document.createElement('ul');
            ul.setAttribute('class', 'userlist');

            for(var user of this.users){
                ul.appendChild(user['element']);
            }

            this.element.innerHTML = "";
            this.element.appendChild(ul);
        };

        queryJson('', {}, this.populateUsers.bind(this));
    }

    window.UserList = UserList;

})();
