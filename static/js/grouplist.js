'use strict';

(function(){

    var GroupList = function(containerId, listProvider, buildCallback){
        BaseList.call(this, containerId, buildCallback);
        queryJson(listProvider, {}, this.populate.bind(this));
    };

    GroupList.prototype = Object.create(BaseList.prototype, {
        populate: {
            value: function(json){
                this.elems = json['groups'];
                for(var i in this.elems){
                    var group = this.elems[i];
                    var pictureContainer = document.createElement('div');
                        pictureContainer.setAttribute('class', 'picture_container');
                        pictureContainer.setAttribute('style', 'background-color: ' + group['color']);
                    var nameContainer = document.createElement('div');
                        nameContainer.appendChild(document.createTextNode(group['name']));
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    group.element = document.createElement('li');
                    group.element.appendChild(pictureContainer);
                    group.element.appendChild(nameContainer);
                    group.element.appendChild(actionContainer);
                    if(this.onElemBuild){
                        var actions = this.onElemBuild(group);
                        for(var i in actions){
                            actionContainer.appendChild(actions[i].element);
                        }
                    }
                    this.listelement.appendChild(group.element);
                }

                this.matchingElems = this.elems;
                this.matchingElems.sort(function(a, b){
                    var nameA = a['name'].toLowerCase();
                    var nameB = b['name'].toLowerCase();

                    if(nameA > nameB) return 1;
                    else if(nameA < nameB) return -1;
                    else return 0;
                });

                this.render();
            },
        },

        match: {
            value: function(group){
                var match = false;
                var regex = this.cachedSearchRegex;
                match |= regex.test(group['name']);
                return match;
            },
        },
    });

    window.GroupList = GroupList;
    window.GroupList.GroupAction = Action;

})();
