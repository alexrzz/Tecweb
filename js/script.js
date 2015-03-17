function generaNews(){
  if (window.XMLHttpRequest)
            {// code for IE7+, Firefox, Chrome, Opera, Safari
                xmlhttp=new XMLHttpRequest();
            }
            else
            {// code for IE6, IE5
                xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
            }



            xmlhttp.onload = function() {
                var xmlDoc = new DOMParser().parseFromString(xmlhttp.responseText,'text/xml');

                console.log(xmlDoc);

                document.write("<dl>");
                var x=xmlDoc.getElementsByTagName("notizia");
                for (i=x.length-1;i>x.length-5;i--)
                { 
                    document.write("<dt>");
                    document.write(x[i].getElementsByTagName("data")[0].childNodes[0].nodeValue);
                    document.write("<dd>");
                    document.write(x[i].getElementsByTagName("titolo")[0].childNodes[0].nodeValue);
                    document.write("</dd></dt>");
                }
                document.write("</dl>");

            }


            xmlhttp.open("GET","xml/notizie.xml",false);
            xmlhttp.send();
}
    
		
function validate(input, pattern)
{
    var errorCode=0;
    /* ERROR CODE
     * 0: valore valido
     * 1: valore vuoto o non definito
     * 2: valore in formato non valido rispetto al pattern
     * */
    if(input == null || input == "") {errorCode=1;}
    else if(pattern != null && !pattern.test(input)) {errorCode=2;}
    return errorCode;
}

function aggiungiErrore(lista, errore) {
    var errorMsg = document.createTextNode(errore);
    var errorItem = document.createElement("li");
    errorItem.appendChild(errorMsg);
    lista.appendChild(errorItem);
}

function checkRegistration() {
    var errori = document.getElementById("ul_riserv");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["registrazione"];
    var validationError = false;
    var patternMail = /^[\w\-\+\.]+@[\w\-\+\.]+\.[\w\-\+\.]+$/;
    var patternTelefono = /^\d+$/;
    var patternUsername = /^\S{3,}$/;
    var deniedUsername = /^([^!@#^&*èòàùì]+)$/;
    var patternPassword = /\S{6,}/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "ul_riserv");
    
    if(input["nome"].value == null || input["nome"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Nome' è obbligatorio");
        validationError = true;
    }
    if(input["cognome"].value == null || input["cognome"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Cognome' è obbligatorio");
        validationError = true;
    }
    switch( validate(input["telefono"].value,patternTelefono) )
    {
      case 1: aggiungiErrore(errorList, "Il campo 'Telefono' è obbligatorio"); validationError=true; break;
      case 2: aggiungiErrore(errorList, "Il campo 'Telefono' deve essere costituito da soli numeri."); validationError=true; break;
    }
    switch( validate(input["mail"].value,patternMail) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Posta elettronica' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Posta elettronica' contiene un indirizzo di posta elettronica non valido"); validationError=true; break;
    }
    switch( validate(input["username"].value,patternUsername) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Nome utente' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Nome utente' deve contenere almeno 3 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    switch( validate(input["username"].value,deniedUsername) )
    {
        case 2: aggiungiErrore(errorList, "Il campo 'Nome utente' contiene caratteri non ammessi (^!@#^&*èàòìù)."); validationError=true; break;
    }
    switch( validate(input["password"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Password' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Password' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    switch( validate(input["repass"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Conferma password' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Conferma password' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    if(input["password"].value != input["repass"].value)
    {
        aggiungiErrore(errorList, "Le password indicate non coincidono!");
        validationError = true;
    }
    if(validationError) {
        var form = document.getElementById("registrazione");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    } else return true;
}

function checkLogin() {
    var errori = document.getElementById("ul_riserv");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["login"];
    var validationError = false;
    var patternUsername = /^\S{3,}$/;
    var patternPassword = /\S{6,}/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "ul_riserv");
    
    switch( validate(input["username"].value,patternUsername) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Nome utente' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Nome utente' deve contenere almeno 3 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    switch( validate(input["password"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Password' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Password' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    if(validationError) {
        var form = document.getElementById("login");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    }
    else return true;
}

function checkQuestion(){
  var errori = document.getElementById("ul_riserv");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["chiedi"];
    var validationError = false;
    var patternQuestion = /^([^!@#^&*]+)$/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "ul_riserv");
    
    switch( validate(input["domanda"].value,patternQuestion) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Domanda' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Domanda' contiene un carattere non ammesso (!@#$%^&*)"); validationError=true; break;
    }
    if(validationError) {
        var form = document.getElementById("chiedi");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    }
    else return true;
}

function checkAddNews(){
  var errori = document.getElementById("ul_riserv");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["add_news"];
    var validationError = false;
    var patternNews = /^([^!@#^&*]+)$/;
    
    var values = input["data"].value.split("-");
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "ul_riserv");
    
    if(input["categoria"].value == null || input["categoria"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Categoria' è obbligatorio");
        validationError = true;
    }
    if(input["data"].value == null || input["data"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Data' è obbligatorio");
        validationError = true;
    }
    else{
	  if(values[2].length!=2 || values[1].length!=2 || values[0].length!=4)
	  {
	    aggiungiErrore(errorList, "Formato data errato. Inserire nella forma aaaa-mm-gg.");
	    validationError = true;
	  }
	  else{
	    if(values[2]>31 || values[2]<1)
	    {
	      aggiungiErrore(errorList, "I giorni nel campo data devono essere compresi tra 1 e 31.");
	      validationError = true;
	    }
	    if(values[1]>12 || values[1]<1)
	    {
	      aggiungiErrore(errorList, "I mesi nel campo data devono essere compresi tra 1 e 12.");
	      validationError = true;
	    }
	  }
    }
    
    if(input["titolo"].value == null || input["titolo"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Titolo' è obbligatorio");
        validationError = true;
    }
    
        switch( validate(input["descrizione"].value,patternNews) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Descrizione' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Descrizione' contiene un carattere non ammesso (!@#$%^&*)"); validationError=true; break;
    }
    if(validationError) {
        var form = document.getElementById("add_news");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    }
    else return true;
}

function checkAddAnswer(){
  var errori = document.getElementById("ul_riserv");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["rispondi"];
    var validationError = false;
    var patternQuestion = /^([^!@#^&*]+)$/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "ul_riserv");
    
    switch( validate(input["risp"].value,patternQuestion) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Risposta' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Risposta' contiene un carattere non ammesso (!@#$%^&*)"); validationError=true; break;
    }
    if(validationError) {
        var form = document.getElementById("rispondi");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    }
    else return true;
}

function checkEditUser(){
        var errori = document.getElementById("ul_riserv");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["edit_user"];
    var validationError = false;
    var patternMail = /^[\w\-\+\.]+@[\w\-\+\.]+\.[\w\-\+\.]+$/;
    var patternTelefono = /^\d+$/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "ul_riserv");
    
    if(input["nome"].value == null || input["nome"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Nome' è obbligatorio");
        validationError = true;
    }
    if(input["cognome"].value == null || input["cognome"].value == "")
    {
        aggiungiErrore(errorList, "Il campo 'Cognome' è obbligatorio");
        validationError = true;
    }
    switch( validate(input["telefono"].value,patternTelefono) )
    {
      case 1: aggiungiErrore(errorList, "Il campo 'Telefono' è obbligatorio"); validationError=true; break;
      case 2: aggiungiErrore(errorList, "Il campo 'Telefono' deve essere costituito da soli numeri."); validationError=true; break;
    }
    switch( validate(input["mail"].value,patternMail) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Posta elettronica' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Posta elettronica' contiene un indirizzo di posta elettronica non valido"); validationError=true; break;
    }
    if(validationError) {
        var form = document.getElementById("edit_user");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    } else return true;
}
