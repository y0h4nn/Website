window.addEventListener('load', function(){
    max = document.getElementById('id_max_inscriptions').parentNode;
    limited = document.getElementById('id_limited');
    function check_max(){
        if(limited.checked){
            max.style.display = "flex";
        }
        else{
            max.style.display = "none";
        }
    }
    limited.addEventListener('change', function(){
        check_max();
    });
    check_max();
});
