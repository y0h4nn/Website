"use strict";


/*
 * Base popup
 */

function Popup(title){
    // Popup init
    this.container = document.createElement('div');
    this.container.setAttribute('class', this.baseClass);
    this.window = document.createElement('div');
    this.header = document.createElement('header');
    this.h1 = document.createElement('h1');
    this.h1.appendChild(document.createTextNode(title));
    this.closeBtn = document.createElement('button');
    this.closeBtn.innerHTML = "<i class='fa fa-close'></i>";
    this.closeBtn.setAttribute('type', 'button');
    this.main = document.createElement('main');

    document.body.insertBefore(this.container, document.body.firstChild);
    this.container.appendChild(this.window);
    this.window.appendChild(this.header);
    this.header.appendChild(this.h1);
    this.header.appendChild(this.closeBtn);
    this.window.appendChild(this.main);

    this.container.addEventListener('click', function(event){
        if(!this.window.contains(event.target)){
            this.close();
        }
    }.bind(this));

    this.closeBtn.addEventListener('click', function(event){
        this.close();
    }.bind(this));
}

Popup.prototype = {
    baseClass: 'popup',
    pop: function(){
        this.container.setAttribute('class', this.baseClass + ' pop');
    },

    close: function(){
        this.container.setAttribute('class', this.baseClass);
        if(this.onClose != undefined){
            this.onClose();
        }
    }
}


/*
 * Selection popup
 *
 * Open a pupop with the given choices and call the callback with the selected
 * one as it's first argument. choises is an array with a key as the choice
 * name and the value as the choice displayed
 */

function  SelectionPopup(title, choices, callback){
    Popup.call(this, title);
    this.baseClass = 'selection_popup';
    this.callback = callback;

    for(var choice in choices){
        var button = document.createElement('button');
        button.innerHTML = choices[choice];
        button.setAttribute('data-choice', choice);
        button.setAttribute('type', 'button');
        this.main.appendChild(button);

        button.addEventListener('click', function(event){
            var choice = event.target.getAttribute('data-choice');
            this.callback(choice);
            this.close();
        }.bind(this));
    }
}

SelectionPopup.prototype = Object.create(Popup.prototype, {
});

SelectionPopup.prototype.constructor = SelectionPopup;


/*
 * RemoteHtmlPopup
 *
 * takes the remote content url and display fetched content in the popup
 */

function RemoteHtmlPopup(title, contentUrl){
    Popup.call(this, title);
    this.spinner = document.createElement('div');
    this.spinner.setAttribute('class', 'spinner');
    this.spinner.innerHTML = 'Not done yet';

    this.main.appendChild(this.spinner);
    this.fetch(contentUrl);
}

RemoteHtmlPopup.prototype = Object.create(Popup.prototype, {
    fetch: {
        value: function(url){
            var xhr = new XMLHttpRequest();
            xhr.open('get', url);
            xhr.onreadystatechange = function(){
                if(xhr.readyState == xhr.DONE){
                    this.updateContent(xhr.responseText);
                }
            }.bind(this);
            xhr.send();
        },
    },

    updateContent: {
        value: function(rawHtml){
            this.main.innerHTML = rawHtml;
        },
    },


});

RemoteHtmlPopup.prototype.constructor = RemoteHtmlPopup;


/*
 * User selection popup
 */

function UserSelectionPopup(title, callback){
    Popup.call(this, title);
    this.users = [];
    this.callback = callback;
    this.baseClass = 'user_selection_popup';
    this.searchInput = document.createElement('input');
    this.btnContainer = document.createElement('div');
    this.spinner = document.createElement('div');
    this.spinner.setAttribute('class', 'spinner');
    this.main.appendChild(this.searchInput);
    this.main.appendChild(this.spinner);
    this.main.appendChild(this.btnContainer);
    this.fetchList();
    this.cachedSearchRegex = new RegExp('');
    this.matchingUsers = []


    this.searchInput.addEventListener('keyup', function(){
        if(this.timer){
            clearTimeout(this.timer);
        }
        this.timer = setTimeout(function(){
            this.updateFilter();
            this.buildUserList(this.matchingUsers);
        }.bind(this), 100);
    }.bind(this));
}

UserSelectionPopup.prototype = Object.create(Popup.prototype, {
    updateFilter: {
        value: function(){
            var pattern = this.searchInput.value.split('').join('.*?');
            this.cachedSearchRegex = new RegExp(pattern, 'i');
            this.matchingUsers = this.users.filter(this.match, this);
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

    buildUserList: {
        value: function(users){
            this.btnContainer.innerHTML = "";
            for(var i in users){
                var user = users[i];
                var text = document.createTextNode(user.display_name);
                var button = document.createElement('button');
                button.appendChild(text);
                button.setAttribute('type', 'button');
                button.setAttribute('data-uid', user.id);
                button.addEventListener('click', function(event){
                    var uid = event.target.getAttribute('data-uid');
                    this.callback(uid);
                    this.close();
                }.bind(this));
                this.btnContainer.appendChild(button);
            }
            this.spinner.setAttribute('class', 'hidden');
            this.searchInput.focus();
        },
    },

    fetchList: {
        value: function(){
            var xhr = new XMLHttpRequest();
            xhr.open('OPTIONS', '/accounts/members/');
            xhr.onreadystatechange = function(){
                if(xhr.readyState == xhr.DONE){
                    this.users = JSON.parse(xhr.responseText)['users']
                    this.buildUserList(this.users);
                }
            }.bind(this);
            xhr.send();
        },
    },

});

UserSelectionPopup.prototype.constructor = UserSelectionPopup;


/*
 * User list popup
 */

function UserListPopup(title, listProvider, buildCallback){
    Popup.call(this, title);
    this.userListContainer = document.createElement('div');
    this.userListContainer.id = 'userlist_popup';
    this.main.appendChild(this.userListContainer);
    this.userList = new UserList(this.userListContainer.id, listProvider, buildCallback);
}

UserListPopup.prototype = Object.create(Popup.prototype, {
});

UserListPopup.prototype.constructor = UserListPopup;


/*
 * Photo popup
 */

function DiaporamaPopup(images){
    this.images = images;
    this.index = 0;
    this.container = document.createElement('div');
    this.container.setAttribute('class', this.baseClass);

    this.image = document.createElement('img');

    this.overlay = document.createElement('div');

    this.nextButton = document.createElement('button');
    this.nextButton.setAttribute('type', 'button');
    this.nextButton.innerHTML = "<i class='fa fa-chevron-right'></i>";

    this.previousButton = document.createElement('button');
    this.previousButton.setAttribute('type', 'button');
    this.previousButton.innerHTML = "<i class='fa fa-chevron-left'></i>";

    this.downloadButton = document.createElement('button');
    this.downloadButton.setAttribute('type', 'button');
    this.downloadButton.innerHTML = "<i class='fa fa-download'></i>";

    document.body.insertBefore(this.container, document.body.firstChild);
    this.container.appendChild(this.image);
    this.container.appendChild(this.overlay);
    this.overlay.appendChild(this.previousButton);
    this.overlay.appendChild(this.downloadButton);
    this.overlay.appendChild(this.nextButton);

    this.container.addEventListener('click', function(event){
        console.log(event.target, this.previousButton, this.nextButton);
        if(!this.overlay.contains(event.target)){
            this.close();
        }
    }.bind(this));

    this.downloadButton.addEventListener('click', function(event){
        var url = this.images[this.index];
        console.log(url);
        document.location.href = url;
    }.bind(this));

    this.nextButton.addEventListener('click', this.nextImage.bind(this));
    this.previousButton.addEventListener('click', this.previousImage.bind(this));

    document.addEventListener('keyup', function(event){
        switch(event.keyCode){
            case 39:
                this.nextImage();
                break;
            case 37:
                this.previousImage();
                break;
            case 27:
                this.close();
                break;
        }
    }.bind(this));
}

DiaporamaPopup.prototype = Object.create(Popup.prototype, {
    baseClass: {
        value: 'diaporama_popup',
    },
    selectImage: {
        value: function(index){
            this.index = this.normalizedIndex(index);
            this.image.src = this.images[this.index];
            this.prefetchImage(this.index - 1);
            this.prefetchImage(this.index + 1);
        },
    },

    nextImage: {
        value: function(){
            this.selectImage(this.index + 1);
        },
    },

    previousImage: {
        value: function(){
            this.selectImage(this.index - 1);
        },
    },

    prefetchImage: {
        value: function(index){
            var img = new Image();
            img.src = this.images[this.normalizedIndex(index)];
        },
    },

    normalizedIndex: {
        value: function(index){
            return index % this.images.length + this.images.length * (Math.sign(index) === -1);
        },
    },
});


DiaporamaPopup.prototype.constructor = DiaporamaPopup;
