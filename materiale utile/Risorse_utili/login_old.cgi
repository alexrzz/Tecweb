#!/usr/bin/perl

# NOME
# login.cgi

# DESCRIZIONE
# Gestisce la fase di autenticazione utente (e di creazione di una sessione).

# QUERY STRING
# username, password, javascript

use CGI;
use CGI::Session;
use XML::LibXML;
use Digest::MD5 qw(md5_hex);

# [NOTA IMPORTANTE] La pagina di login può essere raggiunta in tre casi:
# tramite un link diretto, redirezionati da una pagina accessibile solo agli
# utenti autenticati oppure redirezionati dalla pagina di login stessa
# (quest'ultimo caso si verifica quando il login non ha avuto successo). Nel
# primo e nel secondo caso, si stampa semplicemente la pagina di login; nel
# terzo caso, si stampa la pagina di login con segnalati gli errori riscontrati.

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
    # Leggo i valori ricevuti in input (se presenti): pagina di provenienza,
    # username, password e JavaScript.
    my $cgi=new CGI;
    my $source=$cgi->param('source');
    my $username=$cgi->param('username');
    my $password=$cgi->param('password');
    my $javascript=$cgi->param('javascript');
    if(!defined($username) || !defined($password)){
        # prima invocazione della pagina
        if(!defined($source)){
            $source="account.cgi";
        }
        &print_login_page($source,undef);
    }
    else{
        # seconda (o successiva) invocazione della pagina
        # (2) VALIDAZIONE INPUT (JAVASCRIPT DISABILITATO)
        # Se JavaScript è disabilitato lato client, valido i valori in input secondo
        # i seguenti vincoli:
        # - nessuno dei campo dati deve essere vuoto;
        # - lo username deve contenere almeno 3 caratteri qualsiasi, spazi esclusi;
        # - la password deve contenere almeno 6 caratteri qualsiasi, spazi esclusi.
        my $error;
        my $correct_input=1;
        if(defined($javascript)){
            $error="\t\t<ul>\n";
            if($username eq ""){
                $error=$error."\t\t\t<li>Il campo <strong>username</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($username!~/^\S{3,}$/){
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>username</strong> deve contenere almeno 3 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            if($password eq ""){
                $error=$error."\t\t\t<li>Il campo <strong>password</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($password!~/^\S{6,}$/){
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>password</strong> deve contenere almeno 6 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            $error=$error."\t\t</ul>\n";
            if($correct_input==1){
                $error=undef; # ripulisco $error
            }
        }
        if($correct_input==1){
            $password=md5_hex($password);
            my $parser=XML::LibXML->new();
            my $document=$parser->parse_file('xml/utenti.xml');
            my $root=$document->getDocumentElement;
            my @users=$root->findnodes("//utente[username='$username' and password='$password']");
            # (3) GESTIONE AUTENTICAZIONE
            # Se le credenziali d'accesso sono corrette, creo una nuova sessione e
            # redireziono alla pagina di provenienza, altrimenti stampo la pagina di
            # login con segnalato l'errore riscontrato.
            if(@users){
                my $session=CGI::Session->new();
                my $cookie=$cgi->cookie(-name=>$session->name,
                                        -value=>$session->id);
                print $cgi->header(-cookie=>$cookie);
                $session->param('username',$username);
                $session->param('password',$password);
                $session->expire('+20m'); # scadenza della sessione = 20 minuti
                &redirect($source); # non utilizzare $cgi->redirect($url) perché accetta solo URL assoluti
            }
            else{
                $error="\t\t<p>Nome utente e password inserite non corrispondono ad alcun utente registrato.</p>";
                &print_login_page($source,$error);
            }
        }
        else{
            &print_login_page($source,$error);
        }
    }
}

# FUNZIONE N°1: STAMPA PAGINA LOGIN
sub print_login_page{
    print "Content-type: text/html\n\n";
    # prima parte del codice XHTML della pagina
print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="COMPLETARE" name="title" />
    <meta content="COMPLETARE" name="author" />
    <meta content="COMPLETARE" name="description" />
    <meta content="COMPLETARE" name="copyright" />
    <meta content="COMPLETARE" name="keyword" />
    <title>Autenticazione - Cinema Paradiso</title>
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
        <p>Sei in: <a href="../default.html" title="">Pagina iniziale</a> &#187; Autenticazione</p>
    </div>
    <div id="content">
        <h1>Autenticazione</h1>
HTML
    # eventuali messaggi d'errore per l'utente
    if(defined($_[1])){
        print $_[1];
    }
    # seconda parte del codice XHTML della pagina
print <<HTML;
        <form action="login.cgi" method="post" id="login">
            <fieldset>
                <legend>Inserisci le tue credenziali</legend>
                <label for="username">Nome utente</label>
                <input id="username" name="username" />
                <label for="password">Password</label>
                <input type="password" id="password" name="password" />
                <input type="hidden" id="source" name="source" value="$_[0]" readonly="readonly" />
                <input type="reset" value="Cancella tutto" />
                <input type="submit" value="Accedi" onclick="return checkLogin()" />
            </fieldset>
            <noscript>
            <fieldset class="script">
                <input type="text" id="javascript" name="javascript" value="false" readonly="readonly" />
            </fieldset>
            </noscript>
        </form>
        <p>
            <a href="../registrazione.html" title="Registrazione">Non hai un account? Registrati, &egrave; gratis!</a>
        </p>
    </div>
    <div id="footer">
        <p>Cinema Paradiso - Via Guardiani della Notte, 15 (AR)</p>
    </div>
</body>
</html>
HTML
}

# FUNZIONE N°2: REDIREZIONE
sub redirect{
    print "Content-type: text/html\n\n";
    # codice XHTML della pagina
print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
HTML
    if($_[0] eq 'account.cgi'){
        print "\t\t<meta http-equiv='refresh' content='0;url=$_[0]' />\n";
    }
    else{
    print "\t\t<meta http-equiv='refresh' content='0;url=spettacolo.cgi?id=$_[0]' />\n"
;    }
print <<HTML;
</head>
<body>
<body />
</html>
HTML
}