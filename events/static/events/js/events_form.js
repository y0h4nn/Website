window.addEventListener('load', function(){
    max = document.getElementById('id_max_inscriptions').parentNode;
    limited = document.getElementById('id_limited');

    invits = document.getElementById('id_allow_invitations');
    max1 = document.getElementById('id_max_invitations').parentNode;
    max2 = document.getElementById('id_max_invitations_by_person').parentNode;
    is_start = document.getElementById('id_invitations_start_0').parentNode;
    function check_max(){
        if(limited.checked){
            max.style.display = "flex";
        }
        else{
            max.style.display = "none";
        }
    }

    function check_invits(){
        if(invits.checked){
            max1.style.display = "flex";
            max2.style.display = "flex";
            is_start.style.display = "flex"
        }
        else{
            max1.style.display = "none";
            max2.style.display = "none";
            is_start.style.display = "none"
        }
    }

    limited.addEventListener('change', function(){
        check_max();
    });

    invits.addEventListener('change', function(){
        check_invits();
    });
    check_max();
    check_invits();
});
