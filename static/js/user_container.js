
window.addEventListener('load', function(){
  var button = document.getElementById('toggle_user_container');
  var explicitClose = false;
  var explicitOpen = false
  var previousSize = document.body.clientWidth;

  function retract(){
      document.body.setAttribute('class', 'retracted')
      button.firstChild.setAttribute('class', 'fa fa-chevron-left');
      localStorage.setItem('userContainerRetracted', true);
  }
  function expand(){
      document.body.setAttribute('class', '')
      button.firstChild.setAttribute('class', 'fa fa-chevron-right');
      localStorage.setItem('userContainerRetracted', false);
  }

  button.addEventListener('click', function(event){
    if(document.body.getAttribute('class') == 'retracted'){
      expand();
      explicitOpen = true;
    }
    else{
      retract();
      explicitClose = true;
    }
  });

  window.addEventListener('resize', function(event){
    if(document.body.clientWidth < 1280){
      if(document.body.clientWidth < previousSize){
        retract();
      }
    }
    else if (!explicitClose){
      expand();
    }
    previousSize = document.body.clientWidth;
  });


  if(localStorage.getItem('userContainerRetracted') === "true"){
    retract();
    explicitClose = true;
  }

  if(document.body.clientWidth < 1280){
    retract()
  }
  else if (!explicitClose){
    expand()
  }
});
