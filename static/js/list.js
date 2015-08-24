'use strict'

var Action = function(name, callback, toggled){
	this.callback = callback;
	this.element = document.createElement('button');
	this.element.setAttribute('type', 'button');
	this.element.innerHTML = name;

	this.element.addEventListener('click', function(event){
		this.callback(event);
	}.bind(this));

	this.setToggled = function(){
		this.element.setAttribute('class', 'toggled');
	};

	this.setUntoggled = function(){
		this.element.setAttribute('class', '');
	};

	this.toggle = function(){
		if(this.element.getAttribute('class') == 'toggled'){
			this.setUntoggled();
		}
		else{
			this.setToggled();
		}
	};

	this.isToggled = function(){
		if(this.element.getAttribute('class') == 'toggled'){
			return true;
		}
		else{
			return false;
		}
	};

	if(toggled){
		this.setToggled();
	}
};


var BaseList = function(containerId, buildCallback, clickCallback){
	this.element = document.getElementById(containerId);
	this.searchInput = document.createElement('input');
	this.spinner = document.createElement('div');
	this.spinner.setAttribute('class', 'spinner');
	this.listelement = document.createElement('ul');
	this.listelement.setAttribute('class', 'userlist');
	this.elems = []
	this.matchingElems = []
	this.cachedSearchRegex = new RegExp('');
	this.element.appendChild(this.searchInput);
	this.element.appendChild(this.spinner);
	this.element.appendChild(this.listelement);

	// hooks
	this.onElemBuild = buildCallback;
	this.onClick = clickCallback;

	this.render = function(){
		this.spinner.setAttribute('class', 'spinner hidden');

		for(var elem of this.elems){
			if(this.matchingElems.indexOf(elem) >= 0){
				elem.element.className = '';
			}
			else{
				elem.element.className = 'hidden';
			}
		}
	};

	this.updateElems = function(){
			var pattern = this.searchInput.value.split('').join('.*?');
			this.cachedSearchRegex = new RegExp(pattern, 'i');

			this.matchingElems = this.elems.filter(this.match, this);
	};

	this.searchInput.addEventListener('keyup', function(){
		if(this.timer){
			clearTimeout(this.timer);
		}
		this.timer = setTimeout(function(){
			var startDate = new Date();
			this.updateElems();
			this.render();
			console.log("Search update and rendering in " + (new Date() - startDate + "ms"));
		}.bind(this), 100);
	}.bind(this));
}
