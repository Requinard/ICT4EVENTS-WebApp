$(document).ready(function() {
   $('#form-field-search').keypress(function(e){
       // This is enter
       if(e.charCode === 13)
       {
           var text = e.currentTarget.value;
           text = text.replace(' ', '+');
           var url = "/search/"
           window.location = url + text + "/"
       }
   })
});