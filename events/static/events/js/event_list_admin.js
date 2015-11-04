'use strict';


(function(){
    var EventList = function(containerId, arg, buildCallback, clickCallback){
        BaseList.call(this, containerId, buildCallback, clickCallback);
        queryJson('list/', {"arg": arg}, this.populate.bind(this));
    };

    EventList.prototype = Object.create(BaseList.prototype, {
        populate: {
            value: function(data){
                this.elems = data['events'];
                for(var i in this.elems){
                    var evt = this.elems[i];
                    var img = document.createElement('img');
                        img.setAttribute('src', evt['picture']);
                        img.setAttribute('alt', 'profile_picture');
                    var pictureContainer = document.createElement('div');
                        pictureContainer.setAttribute('class', 'picture_container');
                    var nameContainer = document.createElement('div');
                    var d = new Date(evt['start_time']);
                    var dateContainer = document.createElement('span');
                        dateContainer.setAttribute('style', 'color: #BBB');
                        dateContainer.innerHTML = ' (' + d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear() + ')';
                        nameContainer.appendChild(document.createTextNode(evt['name']));
                        nameContainer.appendChild(dateContainer);
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    evt.element = document.createElement('li');
                    evt.element.appendChild(pictureContainer);
                    evt.element.appendChild(nameContainer);
                    evt.element.appendChild(actionContainer);
                    if(this.onElemBuild){
                        var actions = this.onElemBuild(evt);
                        for(var i in actions ){
                            actionContainer.appendChild(actions[i].element);
                        }
                    }
                    pictureContainer.appendChild(img);
                    this.listelement.appendChild(evt.element);
                }
                this.matchingElems = this.elems;
                this.matchingElems.sort(function(a, b){
                    var nameA = new Date(a['start_time']);
                    var nameB = new Date(b['start_time']);

                    if(nameA > nameB) return 1;
                    else if(nameA < nameB) return -1;
                    else return 0;
                });
                this.render();
            },
        },
        match: {
            value: function(elmt) {
                var match = false;
                var regex = this.cachedSearchRegex;
                match |= regex.test(elmt['name']);
                match &= !elmt['deleted'];
                return match
            },
        },

    });

    window.EventList = EventList;
    window.EventList.Action = Action;
})();
