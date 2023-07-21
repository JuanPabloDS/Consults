$(function () {


    //HEADER
    $(window).scroll(function () {
          if($(this).scrollTop() > 200)
          {
              if (!$('.main_header').hasClass('fixed'))
              {
                  $('.main_header').stop().addClass('fixed').css('top', '-100px').animate(
                      {
                          'top': '0px'
                      }, 500);
              }
          }
          else
          {
              $('.main_header').removeClass('fixed');
          }
    });


});

function mask(o,f){
    v_obj=o
    v_fun=f
    setTimeout("execmask()",1)
}

function execmask(){
    v_obj.value=v_fun(v_obj.value)
}

function maskcnpj(v){
    v=v.replace(/\D/g,"");
    v=v.replace(/^(\d{2})(\d)/,"$1.$2");
    v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3");
    v=v.replace(/\.(\d{3})(\d)/,".$1/$2");
    v=v.replace(/(\d{4})(\d)/,"$1-$2");
    return v;
    }

function masktel(v){
    v=v.replace(/\D/g,"");
    v=v.replace(/^(\d{2})(\d)/g,"($1) $2");
    v=v.replace(/(\d)(\d{4})$/,"$1-$2");
    return v;
    }



function idcss( cnpj ){
    return document.getElementById( cnpj );
}

function idtel( telefone ){
    return document.getElementById( telefone );
}

if (idcss('cnpj') == null){


}else{
    window.onload = function(){

        //CNPJ --------
        idcss('cnpj').setAttribute('maxlength', 18);
        idcss('cnpj').onkeypress = function(){
            mask( this, maskcnpj );
        }
        //-------------
        if (idtel('telefone') == null){
        }else{

            //CELULAR -------
            idtel('telefone').setAttribute('maxlength', 15);
            idtel('telefone').onkeypress = function(){
                mask( this, masktel );
            }
        }
         //-------------

    }
}




function AbrirSecao(secao){
    window.open(""+secao+"", "_parent");
}



function pergunta(){
    // retorna true se confirmado, ou false se cancelado
    return confirm('Tem certeza que deseja excluir?');
 }


 function finalizar(){
    // retorna true se confirmado, ou false se cancelado
    return confirm('Tem certeza que deseja finalizar o treinamento?');
 }

 function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn2')) {
      var dropdowns = document.getElementsByClassName("dropdown-content2");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }


function submitForm() {
    let form = document.getElementById("form__submit");
    form.submit();
}


// MENU

class MobileNavbar {
    constructor(mobileMenu, mobileMenuex, navList, navLinks) {
      this.body = document.querySelector("body");
      this.mobileMenu = document.querySelector(mobileMenu);
      this.mobileMenuEx = document.querySelector(mobileMenuex);
      this.navList = document.querySelector(navList);
      this.navLinks = document.querySelectorAll(navLinks);
      this.activeClass = "active";
      this.hiddenClass = "hidden";
  
      this.handleClick = this.handleClick.bind(this);
    }
  
    animateLinks() {
      this.navLinks.forEach((link, index) => {
        link.style.animation
          ? (link.style.animation = "")
          : (link.style.animation = `navLinkFade 0.5s ease forwards ${
              index / 7 + 0.3
            }s`);
      });
    }
  
    handleClick() {
      this.navList.classList.toggle(this.activeClass);
      this.mobileMenu.classList.toggle(this.activeClass);
      this.body.classList.toggle(this.hiddenClass);
      this.mobileMenuEx.classList.toggle(this.activeClass);
      this.animateLinks();
    }
  
    addClickEvent() {
      this.mobileMenu.addEventListener("click", this.handleClick);
      this.mobileMenuEx.addEventListener("click", this.handleClick);
    }
  
    init() {
      if (this.mobileMenu) {
        this.addClickEvent();
      }
      return this;
    }
  }
  
  const mobileNavbar = new MobileNavbar(
    ".mobile-menu",
    ".mobile-menu-ex",
    ".nav-list",
    ".nav-list li",
  );


  mobileNavbar.init();

  


// Apagar espaço em branco no cadastro do usuario

function validarInput() {
  var inputElement = document.getElementById("user");
  var texto = inputElement.value;
  var padrao = /^[a-zA-Z0-9]+$/;  // Apenas letras maiúsculas, minúsculas e números são permitidos

  if (!padrao.test(texto)) {
    alert("O campo 'Usuário' contém espaços ou caracteres especiais.");
    inputElement.value = "";
    inputElement.focus();
  }
}



// MENU3

function toggleMenu3() {
  var menuItems = document.getElementById("menuItems3");
  menuItems.classList.toggle("show3");
}

// Fechar o menu quando clicar fora dele
window.onclick = function(event) {
  var menuItems = document.getElementById("menuItems3");
  if (!event.target.matches('.menu-button3')) {
    if (menuItems.classList.contains('show3')) {
      menuItems.classList.remove('show3');
    }
  }
};