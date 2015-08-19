"use strict";

(function(){
    var SelectionPopup = function(title, choices, callback){
        this.callback = callback;
        this.container = document.createElement('div');
        this.container.setAttribute('class', 'selection_popup');
        this.window = document.createElement('div');
        this.title = document.createElement('h1');
        this.title.innerHTML = title;

        document.body.insertBefore(this.container, document.body.firstChild);
        this.container.appendChild(this.window);
        this.window.appendChild(this.title);


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

        this.pop = function(){
            this.container.setAttribute('class', 'selection_popup pop');
        };

        this.close = function(){
            this.container.setAttribute('class', 'selection_popup');
        };

        this.container.addEventListener('click', function(event){
            if(!this.window.contains(event.target)){
                this.close();
                console.log("Close popup");
            }
        }.bind(this));
    };

    window.SelectionPopup = SelectionPopup;
})();
