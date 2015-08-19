"use strict";


/*
 * Base popup
 */

function Popup(){
    // Popup init
    this.container = document.createElement('div');
    this.container.setAttribute('class', this.popupClass);
    this.window = document.createElement('div');

    document.body.insertBefore(this.container, document.body.firstChild);
    this.container.appendChild(this.window);

    this.container.addEventListener('click', function(event){
        if(!this.window.contains(event.target)){
            this.close();
            console.log("Close popup");
        }
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
    Popup.call(this);
    this.baseClass = 'selection_popup';

    this.title = document.createElement('h1');
    this.title.innerHTML = title;
    this.window.appendChild(this.title);
    this.callback = callback;

    for(var choice in choices){
        var button = document.createElement('button');
        button.innerHTML = choices[choice];
        button.setAttribute('data-choice', choice);
        button.setAttribute('type', 'button');
        this.window.appendChild(button);

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

function RemoteHtmlPopup(contentUrl){
    Popup.call(this);
    this.spinner = document.createElement('div');
    this.spinner.setAttribute('class', 'spinner');
    this.spinner.innerHTML = 'Not done yet';

    this.window.appendChild(this.spinner);
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
            this.window.innerHTML = rawHtml;
        },
    },


});

RemoteHtmlPopup.prototype.constructor = RemoteHtmlPopup;

