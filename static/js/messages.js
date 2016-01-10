function add_message(klass, text, delay){
    if(delay == undefined){
        delay = 5000;
    }
    messages_div = document.getElementById('messages');
    message = document.createElement('div');
    message_icon = document.createElement('i');
    message_span = document.createElement('span');

    if(klass == "error"){
        message_icon.className = "fa fa-exclamation-circle";
    }
    else if(klass == "warning"){
        message_icon.className = "fa fa-check-circle";
    }
    else{
        message_icon.className = "fa fa-info-circle";
    }

    message_span.innerHTML = text;
    message.className = "message " + klass;
    messages_div.appendChild(message);
    message.appendChild(message_icon);
    message.appendChild(message_span);

    function remove(){
        // Avoid error when someone click on it before the setTimeout calls this function.
        if(this.parentNode != null){
            this.parentNode.removeChild(this);
        }
    }

    message.addEventListener('click', function(){
        remove.bind(this)();
    });
    if(delay){
        window.setTimeout(remove.bind(message), delay);
    }
}

