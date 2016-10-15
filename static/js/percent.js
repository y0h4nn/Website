'use strict'

// Coucou, si tu cherches la date du percent, je peux te dire que c'est demain

window.addEventListener('load', function() {
    var percent_span = document.getElementById("percent-date");
    function leftpad(str) {
        var str = "" + str;
        var pad = "00";
        return pad.substring(0, pad.length - str.length) + str;
    }

    function get_percent_date() {
        var now = new Date();
        var percent = new Date(now.getTime() + (24 * 60 * 60 * 1000));
        percent.setHours(0,0,0,0);
        var diff = new Date(percent.getTime() - now.getTime());

        var hours = leftpad(diff.getHours() - 1);
        var minutes = leftpad(diff.getMinutes());
        var seconds = leftpad(diff.getSeconds());

        percent_span.innerHTML = hours + ":" + minutes + ":" + seconds;
      }

    setInterval(get_percent_date, 1000);
    get_percent_date();

});
