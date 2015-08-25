function read(element){
    console.log(element);
    var id = element.getAttribute('data-notification-id');


    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/notifications/read/' + id );
    xhr.onreadystatechange = function(){
        if(xhr.readyState == xhr.DONE){
            // clean up node and set as read
            element.parentNode.innerHTML = "<i class='fa fa-check'> Lu</i>";
        }
    };
    xhr.send();
}
