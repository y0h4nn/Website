
(function(){

	var Email = function(parent){
		this.parent = parent;
		this.p = document.createElement('p');
		this.label = document.createElement('label');
		this.label.innerHTML = "Adresse email supplémentaire";
		this.input = document.createElement('input');
		this.deleteButton = document.createElement('button');
		this.deleteButton.innerHTML = "x";
		this.deleteButton.type = "button"
		this.p.appendChild(this.label);
		this.p.appendChild(this.input);
		this.p.appendChild(this.deleteButton);
		this.parent.element.appendChild(this.p);

		this.deleteButton.addEventListener('click', function(){
			this.parent.element.removeChild(this.p);
		}.bind(this));

		this.input.addEventListener('change', function(){
			console.log("ok");
		}.bind(this));
	}

	var Emails = function(element){
		this.element = element;
		this.addButton = document.getElementById('emails_add');
		this.emails = []

		this.addButton.addEventListener('click', function(event){
			this.emails.push(new Email(this));
		}.bind(this));
	}


	window.addEventListener('load', function(){
		var emailsElement = document.getElementById('emails');
		var addressesElement = document.getElementById('addresses');

		var emails = new Emails(emailsElement);
	});

})();
