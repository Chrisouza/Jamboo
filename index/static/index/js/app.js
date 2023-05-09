$(document).ready(function(){
    $('#cnpj').mask('00.000.000/0000-00');
    $("#telefone").on("blur",function(){
      if(this.value.length == 10 ){
        $("#telefone").mask("(00) 0000-0000");
      } else if(this.value.length == 11) {
        $("#telefone").mask("(00) 0 0000-0000");
      }
    });
    //if($("#telefone").value.length > 11){
    
    //} else {
    //  $("#telefone").mask("(00) 0000-0000");
    //}
    gera_senha()

});

function gera_senha() { 
    var chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ!@#$%^&*()+?><:{}[]";
    var passwordLength = 16;
    var password = "";

    for (var i = 0; i < passwordLength; i++) {
      var randomNumber = Math.floor(Math.random() * chars.length);
      password += chars.substring(randomNumber, randomNumber + 1);
    }
    document.getElementById('senha').value = password
  }