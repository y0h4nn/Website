'use strict';


(function(){
	var EventList = function(containerId, buildCallback, clickCallback){
		BaseList.call(this, containerId, buildCallback, clickCallback);
		queryJson('list/', {}, this.populate.bind(this));
	};

	EventList.prototype = Object.create(EventList, {
		populate: {
			value: function(data){
				this.elems = data['events'];
				for(var evt of this.elems){
					var img = document.createElement('img');
						img.setAttribute('src', evt['picture']);
						img.setAttribute('alt', 'profile_picture');
					var pictureContainer = document.createElement('div');
						pictureContainer.setAttribute('class', 'picture_container');
					var nameContainer = document.createElement('div');
						nameContainer.innerHTML = evt['name'];
					var actionContainer = document.createElement('div');
						actionContainer.setAttribute('class', 'action_container');


					evt.element = document.createElement('li');
					evt.element.appendChild(pictureContainer);
					evt.element.appendChild(nameContainer);
					evt.element.appendChild(actionContainer);
					if(this.onElemBuild){
						for(var action of this.onElemBuild(evt)){
							actionContainer.appendChild(action.element);
						}
					}
					pictureContainer.appendChild(img);
					this.listelement.appendChild(evt.element);
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
				match |= regex.test(elmt['name']);
				match &= !elmt['deleted'];
				return match
			},
		},

	});

	window.EventList = EventList;
    window.EventList.Action = Action;
})();
