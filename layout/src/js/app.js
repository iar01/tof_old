//= ../../node_modules/jquery/dist/jquery.js
//= ../../node_modules/materialize-css/dist/js/materialize.js
//= ../../node_modules/material-design-lite/material.min.js
// //= ../../node_modules/material-modal/dist/js/material-modal.min.js




$(function(){
    $('.modal-trigger').leanModal({
      dismissible: true, // Modal can be dismissed by clicking outside of the modal
      opacity: .5, // Opacity of modal background
      in_duration: 200, // Transition in duration
      out_duration: 200, // Transition out duration      
    }
  );
    
    $('ul.tabs').tabs();
});
