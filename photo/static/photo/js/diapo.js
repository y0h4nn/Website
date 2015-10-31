"use strict";

window.addEventListener('load', function(){
    var images = Array.prototype.slice.call(document.querySelectorAll('img[data-photo-url]'));
    var images_url = images.map(function(image){return image.getAttribute('data-photo-url')});
    var popup = new DiaporamaPopup(images_url);

    for(var i = 0; i < images.length; i++){
        var image = images[i];
        image.addEventListener('click', function(event){
            popup.selectImage(images.indexOf(event.target));
            popup.pop();
        });
    }

});
