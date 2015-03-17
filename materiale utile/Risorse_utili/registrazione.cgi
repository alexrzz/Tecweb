#!/usr/bin/perl

# NOME
# registrazione.cgi

# DESCRIZIONE
# Gestisce la registrazione di un nuovo utente.

# QUERY STRING
# nome, cognome, email, username, password, password_confirm, javascript

use CGI;
use CGI::Session;
use XML::LibXML;
use Digest::MD5 qw(md5_hex);

# (1) VERIFICA AUTENTICAZIONE UTENTE
# Verifico se l'utente è autenticato (in caso affermativo, redireziono alla
# pagina dell'area utente).
$session=CGI::Session->load();
if(!$session->is_expired && !$session->is_empty){
    # utente autenticato
    print "Location: account.cgi\n\n";
}
else{
    # utente non autenticato
    # (2) LETTURA INPUT FORM
    # Leggo i valori ricevuti in input: nome, cognome, email, username, password,
    # conferma della password e JavaScript.
    my $cgi=new CGI;
    my $name=$cgi->param('nome');
    my $surname=$cgi->param('cognome');
    my $email=$cgi->param('email');
    my $username=$cgi->param('username');
    my $password=$cgi->param('password');
    my $password_confirm=$cgi->param('password_confirm');
    my $javascript=$cgi->param('javascript');
    # (2) VALIDAZIONE INPUT (JAVASCRIPT DISABILITATO)
    # Se JavaScript è disabilitato lato client, valido i valori in input secondo i
    # seguenti vincoli:
    # - nessuno dei campo dati deve essere vuoto;
    # - lo username deve contenere almeno 3 caratteri qualsiasi, spazi esclusi;
    # - la password e la relativa conferma devono contenere almeno 6 caratteri
    #   qualsiasi, spazi esclusi;
    # - l'email deve soddisfare il formato standard degli indirizzi di posta
    #   elettronica (ossia x@y, dove x è una sequenza di UNA o più stringhe
    #   separate dal carattere punto '.' e formate da caratteri alfanumerici e dai
    #   caratteri meno '-' e più '+', mentre y è una sequenza di DUE o più
    #   stringhe separate dal carattere punto '.' e formate da caratteri
    #   alfanumerici e dai caratteri meno '-' e più '+').
    # Se i valori in input non superano la validazione, ristampo la pagina di
    # registrazione indicando gli errori riscontrati.
    my $error;
    my $correct_input=1;
    if(defined($javascript)){
        $error="\t\t<ul>\n";
        if($name eq ""){
            $error=$error."\t\t\t<li>Il campo <strong>Nome</strong> &egrave; obbligatorio.</li>\n";
            $correct_input=0;
        }
        if($surname eq ""){
            $error=$error."\t\t\t<li>Il campo <strong>Cognome</strong> &egrave; obbligatorio.</li>\n";
            $correct_input=0;
        }
        if($email eq ""){
            $error=$error."\t\t\t<li>Il campo <strong>Posta elettronica</strong> &egrave; obbligatorio.</li>\n";
            $correct_input=0;
        }elsif($email!~/^[\w\-\+\.]+@[\w\-\+\.]+\.[\w\-\+\.]+$/){
            $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Posta elettronica</strong> deve essere del tipo x\@x.x (dove x rappresenta una sequenza lunga almeno un carattere e formata da caratteri alfanumerici, '-', '+' e '.').</li>\n";
            $correct_input=0;
        }
        if($username eq ""){
            $error=$error."\t\t\t<li>Il campo <strong>Nome utente</strong> &egrave; obbligatorio.</li>\n";
            $correct_input=0;
        }elsif($username!~/^\S{3,}$/){
            $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Nome utente</strong> deve contenere almeno 3 caratteri (spazi non ammessi).</li>\n";
            $correct_input=0;
        }
        if($password eq ""){
            $error=$error."\t\t\t<li>Il campo <strong>Password</strong> &egrave; obbligatorio.</li>\n";
            $correct_input=0;
        }elsif($password!~/^\S{6,}$/){
            $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Password</strong> deve contenere almeno 6 caratteri (spazi non ammessi).</li>\n";
            $correct_input=0;
        }
        if($password_confirm eq ""){
            $error=$error."\t\t\t<li>Il campo <strong>Conferma password</strong> &egrave; obbligatorio.</li>\n";
            $correct_input=0;
        }elsif($password_confirm!~/^\S{6,}$/){
            $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Conferma password</strong> deve contenere almeno 6 caratteri (spazi non ammessi).</li>\n";
            $correct_input=0;
        }
        if($password ne $password_confirm){
            $error=$error."\t\t\t<li>Le password fornite non coincidono.</li>\n";
            $correct_input=0;
        }
        $error=$error."\t\t</ul>\n";
        if($correct_input==1){
            $error=undef; # ripulisco $error
        }
    }
    if($correct_input==1){
        # (3) CONTROLLO USERNAME E REGISTRAZIONE NUOVO UTENTE
        # Se lo username è già utilizzato da un utente registrato, ristampo la
        # pagina di registrazione segnalando l'errore, altrimenti memorizzo le
        # informazioni del nuovo utente, inizializzo una sessione sul server e
        # redireziono alla pagina dell'area utente.
        my $parser=XML::LibXML->new();
        my $document=$parser->parse_file('xml/utenti.xml');
        my $root=$document->getDocumentElement;
        my @registered_users=$root->findnodes("//utente[username='$username']");
        if(@registered_users){
            $error="\t\t\t<p>Username gi&agrave; in uso.</p>";
            &print_registration_page($error,$name,$surname,$email,$username);
        }
        else{
            my $password=md5_hex($password);
            my @users=$root->findnodes("//utenti");
            my $new_user="\t<utente>\n\t\t<nome>$name</nome>\n\t\t<cognome>$surname</cognome>\n\t\t<email>$email</email>\n\t\t<username>$username</username>\n\t\t<password>$password</password>\n\t\t<prenotazioni />\n\t</utente>\n";
            my $fragment=$parser->parse_balanced_chunk($new_user);
            $users[0]->appendChild($fragment); # $users[0] è il nodo 'utenti' (non il primo figlio 'utente' del nodo 'utenti')
            open(OUT,">xml/utenti.xml");
            print OUT $document->toString;
            close(OUT);
            my $session=CGI::Session->new();
            my $cookie=$cgi->cookie(-name=>$session->name,
                                    -value=>$session->id);
            print $cgi->header(-cookie=>$cookie);
            $session->param('username',$username);
            $session->param('password',$password);
            $session->expire('+20m'); # scadenza della sessione = 20 minuti
            &redirect_to_account_page();
        }
    }
    else{
        &print_registration_page($error,$name,$surname,$email,$username);
    }
}

# FUNZIONE N°1: STAMPA PAGINA REGISTRAZIONE
sub print_registration_page{
    print "Content-type: text/html\n\n";
    # prima parte del codice XHTML della pagina
print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="Registrazione utente - Cinema Paradiso" name="title" />
    <meta content="" name="author" />
    <meta content="Pagina di registrazione di un utente" name="description" />
    <meta content="Cinema Paradiso" name="copyright" />
    <meta content="cinema, paradiso, programmazione, film, biglietti, spettacoli, proiezioni" name="keyword" />
    <title>Registrazione utente - Cinema Paradiso</title>
    <link href="../style/screen.css" rel="stylesheet" type="text/css" media="screen" />
    <link href="../style/portable.css" rel="stylesheet" type="text/css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
    <link href="../style/print.css" rel="stylesheet" type="text/css" media="print" />
    <script type="text/javascript" src="../script/validation.js"></script>
    <link rel="shortcut icon" href="../img/cinema.ico" />
</head>
<body>
    <p><a id="skip_nav" href="#content" title="Vai al contenuto" >Vai al contenuto</a></p>
    <div id="header">
        <h1><a href="../default.html" title="Pagina iniziale">Cinema Paradiso</a></h1>
        <h2>Programmazione e prenotazioni online</h2>
    </div>
    <div id="account">
        <p><a href="account.cgi" accesskey="8" title="Area riservata">Area riservata</a> | <a href="../registrazione.html" accesskey="9" title="Registrazione">Registrati</a></p>
    </div>
    <div id="navigation">
        <ul>
            <li><a href="../default.html" accesskey="0">Pagina iniziale</a>
            </li>
            <li><a href="../film.html" accesskey="1">Film</a>
            </li>
            <li><a href="../programmazione.html" accesskey="2">Programmazione</a>
            </li>
            <li><a href="../informazioni.html" accesskey="3">Informazioni</a>
            </li>
            <li><a href="notizie.cgi" accesskey="4">Notizie</a>
            </li>
        </ul>
    </div>
    <div id="path">
        <p>Sei in: <a href="../default.html" title="">Pagina iniziale</a> &#187; Registrazione</p>
    </div>
    <div id="content">
        <h1>Registrazione</h1>
HTML
    # messaggi di avviso per l'utente
    print $_[0];
    # seconda parte del codice XHTML della pagina
print <<HTML;
       <form action="registrazione.cgi" method="post" id="registrazione">
            <fieldset>
                <legend>Informazioni personali</legend>
                <label for="nome">Nome</label>
                <input name="nome" id="nome" value="$_[1]" />
                <label for="cognome">Cognome</label>
                <input id="cognome" name="cognome" value="$_[2]" />
                <label for="email">Posta elettronica</label>
                <input id="email" name="email" value="$_[3]" />
            </fieldset>
            <fieldset>
                <legend>Informazioni del profilo</legend>
                <label for="username">Nome utente</label>
                <input id="username" name="username" value="$_[4]" />
                <label for="password">Password</label>
                <input type="password" id="password" name="password"/>
                <label for="password_confirm">Conferma password</label>
                <input type="password" id="password_confirm" name="password_confirm"/>
                <input type="reset" value="Cancella tutto" />               
                <input type="submit" value="Procedi" />
            </fieldset>
            <noscript>
            <fieldset class="script">
                <input type="text" id="javascript" name="javascript" value="false" readonly="readonly" />
            </fieldset>
            </noscript>
        </form>
        <p class="aiuto">
            Il nome utente e la password devono contenere rispettivamente almeno 3 e 6 caratteri (spazi non ammessi).
            L'indirizzo di posta elettronica dev'essere del tipo <em>utente\@example.org</em>.
        </p>
    </div>
    <div id="footer">
        <p>Cinema Paradiso - Via Guardiani della Notte, 15 (AR)</p>
    </div>
</body>
</html>
HTML
}

# FUNZIONE N°2: REDIREZIONE PAGINA ACCOUNT UTENTE
sub redirect_to_account_page{
    print "Content-type: text/html\n\n";
    # codice XHTML della pagina
print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0; url=account.cgi" />
</head>
</html>
HTML
}