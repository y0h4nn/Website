window.addEventListener('load', function(){
    max_ext = document.getElementById('id_max_extern').parentNode;
    allow_ext = document.getElementById('id_allow_extern');
    function check_max_ext(){
        if(allow_ext.checked){
            max_ext.style.display = "flex";
        }
        else{
            max_ext.style.display = "none";
        }
    }
    allow_ext.addEventListener('change', function(){
        check_max_ext();
    });
    check_max_ext();
});
