"use strict";


/*
 * Base popup
 */

function Popup(title){
    // Popup init
    this.container = document.createElement('div');
    this.container.setAttribute('class', this.popupClass);
    this.window = document.createElement('div');
    this.header = document.createElement('header');
    this.h1 = document.createElement('h1');
    this.h1.innerHTML = title;
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

