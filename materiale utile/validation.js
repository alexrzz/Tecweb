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
    var errori = document.getElementById("errori");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["registrazione"];
    var validationError = false;
    var patternMail = /^[\w\-\+\.]+@[\w\-\+\.]+\.[\w\-\+\.]+$/;
    var patternUsername = /^\S{3,}$/;
    var patternPassword = /\S{6,}/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "errori");
    
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
    switch( validate(input["email"].value,patternMail) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Posta elettronica' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Posta elettronica' contiene un indirizzo di posta elettronica non valido"); validationError=true; break;
    }
    
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
    switch( validate(input["password_confirm"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Conferma password' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Conferma password' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    if(input["password"].value != input["password_confirm"].value)
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
    var errori = document.getElementById("errori");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["login"];
    var validationError = false;
    var patternUsername = /^\S{3,}$/;
    var patternPassword = /\S{6,}/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "errori");
    
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

function updatePassword() {
    var errori = document.getElementById("errori");
    if(errori) {
        var parent = errori.parentNode;
        parent.removeChild(errori);
    }
    var input = document.forms["aggiorna_password"];
    var validationError = false;
    var patternUsername = /^\S{3,}$/;
    var patternPassword = /\S{6,}/;
    
    var errorList = document.createElement("ul");
    errorList.setAttribute("id", "errori");
    
    switch( validate(input["username"].value,patternUsername) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Nome utente' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Nome utente' deve contenere almeno 3 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    switch( validate(input["pwd_corrente"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Password attuale' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Password attuale' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    switch( validate(input["pwd_nuova"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Nuova password' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Nuova password' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    switch( validate(input["pwd_nuova_conferma"].value,patternPassword) )
    {
        case 1: aggiungiErrore(errorList, "Il campo 'Conferma nuova password' è obbligatorio"); validationError=true; break;
        case 2: aggiungiErrore(errorList, "Il campo 'Conferma nuova password' deve contenere almeno 6 caratteri (spazi non ammessi)"); validationError=true; break;
    }
    if(input["pwd_nuova"].value != input["pwd_nuova_conferma"].value)
    {
        aggiungiErrore(errorList, "Le nuove password indicate non coincidono!");
        validationError=true;
    }
    if(validationError) {
        var form = document.getElementById("aggiorna_password");
        (form.parentNode).insertBefore(errorList, form);
        return false;
    } else return true;
}