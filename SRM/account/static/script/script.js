$(document).ready(()=>{
   $(".content1 .container .row .col4 .inner form .form_group #div_id_password1 div[class=''] #id_password1").removeAttr("autocomplete");

   $(".content1 .container .row .col4 .inner form .form_group #div_id_password1 div[class=''] #id_password1").attr("autocomplete","off");

   $(".content1 .container .row .col4 .inner form .form_group #div_id_password1 div[class=''] #id_password2").removeAttr("autocomplete");

   $(".content1 .container .row .col4 .inner form .form_group #div_id_password1 div[class=''] #id_password2").attr("autocomplete","off");



});

document.getElementById('id_username').autocomplete='off';
document.getElementById('id_password1').autocomplete='off';
