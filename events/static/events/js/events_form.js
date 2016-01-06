window.addEventListener('load', function(){
    max = document.getElementById('id_max_inscriptions').parentNode;
    limited = document.getElementById('id_limited');
    management = document.getElementById('id_gestion');
    allow_extern = document.getElementById('id_allow_extern');

    invits = document.getElementById('id_allow_invitations');
    photo_path = document.getElementById('id_photo_path').parentNode;
    max1 = document.getElementById('id_max_invitations').parentNode;
    max2 = document.getElementById('id_max_invitations_by_person').parentNode;
    is_start = document.getElementById('id_invitations_start_0').parentNode;
    extern_end = document.getElementById('id_end_extern_inscriptions_0').parentNode;
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

    function check_photo_path(){
        if(management.value === "NL"){
            photo_path.style.display = "flex";
        }
        else{
            photo_path.style.display = "none";
        }
    }

    function check_extern(){
        if(allow_extern.checked){
            extern_end.style.display = "flex";
        }
        else{
            extern_end.style.display = "none";
        }
    }

    limited.addEventListener('change', function(){
        check_max();
    });

    invits.addEventListener('change', function(){
        check_invits();
    });

    management.addEventListener('change', function(){
        check_photo_path();
    });
    allow_extern.addEventListener('change', function(){
        check_extern();
    });


    check_max();
    check_invits();
    check_photo_path();
    check_extern();

});
