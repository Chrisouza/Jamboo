$(document).ready(function(){
    $('#cnpj').mask('00.000.000/0000-00');
    $("#telefone").mask("(00) 9 0000-0000");
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