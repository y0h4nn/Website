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
				for(var elem of this.elems){
					var img = document.createElement('i');
						img.setAttribute('class', elem['icon']);
					var pictureContainer = document.createElement('div');
						pictureContainer.setAttribute('class', 'picture_container');
					var nameContainer = document.createElement('div');
						nameContainer.innerHTML = elem['title'];
					var actionContainer = document.createElement('div');
						actionContainer.setAttribute('class', 'action_container');


					elem.element = document.createElement('li');
					elem.element.appendChild(pictureContainer);
					elem.element.appendChild(nameContainer);
					elem.element.appendChild(actionContainer);
					if(this.onElemBuild){
						for(var action of this.onElemBuild(elem)){
							actionContainer.appendChild(action.element);
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

