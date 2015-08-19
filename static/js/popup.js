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
            console.log("Close popup");
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
        console.log("POPUP!");
        console.log(this.container.getAttribute('class'));
    },

    close: function(){
        this.container.setAttribute('class', this.baseClass);
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

