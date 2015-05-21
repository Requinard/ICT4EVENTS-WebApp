$(document).ready(function() {
   $('#form-field-search').keypress(function(e){
       // This is enter
       if(e.charCode === 13)
       {
           alert(e);
       }
   })
});