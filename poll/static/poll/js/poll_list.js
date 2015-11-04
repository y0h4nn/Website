'use strict';


(function(){
    var PollList = function(containerId, buildCallback, clickCallback){
        BaseList.call(this, containerId, buildCallback, clickCallback);
        queryJson('list/', {}, this.populate.bind(this));
    };

    PollList.prototype = Object.create(BaseList.prototype, {
        populate: {
            value: function(data){
                this.elems = data['polls'];
                for(var i in this.elems){
                    var elem = this.elems[i];
                    var img = document.createElement('i');
                        img.setAttribute('class', elem['icon']);
                    var pictureContainer = document.createElement('div');
                        pictureContainer.setAttribute('class', 'icon_container');
                    var boldContainer = document.createElement('span');
                        boldContainer.setAttribute('class', 'bold');
                        boldContainer.appendChild(document.createTextNode(elem['title']))
                    var nameContainer = document.createElement('div');
                        nameContainer.appendChild(boldContainer);
                        nameContainer.appendChild(document.createTextNode('(' + elem['start'] + ' - ' + elem['end'] + ')'));
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    elem.element = document.createElement('li');
                    elem.element.appendChild(pictureContainer);
                    elem.element.appendChild(nameContainer);
                    elem.element.appendChild(actionContainer);
                    if(this.onElemBuild){
                        var actions = this.onElemBuild(elem);
                        for(var i in actions){
                            actionContainer.appendChild(actions[i].element);
                        }
                    }
                    pictureContainer.appendChild(img);
                    this.listelement.appendChild(elem.element);
                }
                this.matchingElems = this.elems;
                this.matchingElems.sort(function(a, b){
                    var nameA = a['start_time'];
                    var nameB = b['start_time'];

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
                match |= regex.test(elmt['title']);
                match &= !elmt['deleted'];
                return match
            },
        },

    });

    window.PollList = PollList;
    window.PollList.Action = Action;
})();

