#!/usr/bin/perl

require 'library.pl';

use CGI;
use CGI::Session;
use XML::LibXML;
use Digest::MD5 qw(md5_hex);

$session=CGI::Session->load();
if(!$session->is_expired && !$session->is_empty){
    # utente autenticato
    my $username = $session->param('username');
    &logged_user($username);
}
else{
    my $cgi=new CGI;
    #recupero parametri inserti dall'utente
    my $nome=$cgi->param('nome');
    my $cognome=$cgi->param('cognome');
    my $mail=$cgi->param('mail');
    my $telefono=$cgi->param('telefono');
    my $username=$cgi->param('username');
    my $password=$cgi->param('password');
    my $password_confirm=$cgi->param('repass');
    my $javascript=$cgi->param('javascript');

    if(!defined($username) || !defined($password)){
        # prima invocazione della pagina
        &print_registration(undef,undef,undef,undef,undef,undef);
    }
    else{
    
        my $error;
        my $correct_input=1;
        #controllo sull'input nel caso in cui javascript sia disabilitato
        if(defined($javascript)){
            $error="\t\t<ul id=\"ul_riserv\">\n";
            if($nome eq ""){#controllo se inserito campo nome
                $error=$error."\t\t\t<li>Il campo <strong>Nome</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }
            if($cognome eq ""){#controllo se inserito campo cognome
                $error=$error."\t\t\t<li>Il campo <strong>Cognome</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }
            if($mail eq ""){#controllo se inserito campo mail
                $error=$error."\t\t\t<li>Il campo <strong>Posta elettronica</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($mail!~/^[\w\-\+\.]+@[\w\-\+\.]+\.[\w\-\+\.]+$/){#verifico che sia stata inserita una mail corretta
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Posta elettronica</strong> deve essere del tipo x\@x.x (dove x rappresenta una sequenza lunga almeno un carattere e formata da caratteri alfanumerici, '-', '+' e '.').</li>\n";
                $correct_input=0;
            }
            if($telefono!~/^\d+$/ ){#controllo che il campo telefono sia composto da soli numeri
                $error=$error."\t\t\t<li>Il campo <strong>Telefono</strong> deve essere costituito da soli numeri.</li>\n";
                $correct_input=0;
            }
            if($username eq ""){#controllo se inserito campo username
                $error=$error."\t\t\t<li>Il campo <strong>Nome utente</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($username!~/^\S{3,}$/){#controllo che il campo username contenga almeno 3 caratteri con spazi non ammessi
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Nome utente</strong> deve contenere almeno 3 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            if($username ne "" && $username!~/^([^!@#^&*èòàùì]+)$/){#controllo che il campo username non contenga caratteri speciali o accentati
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Nome utente</strong> contiene caratteri non ammessi (^!@#^&*èàòìù).</li>\n";
                $correct_input=0;
            }
            if($password eq ""){#controllo se inserito campo password
                $error=$error."\t\t\t<li>Il campo <strong>Password</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($password!~/^\S{6,}$/){#controllo che la password contenga almeno 6 caratteri con spazi non ammessi
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Password</strong> deve contenere almeno 6 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            if($password_confirm eq ""){#controllo se inserito campo password di conferma
                $error=$error."\t\t\t<li>Il campo <strong>Conferma password</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($password_confirm!~/^\S{6,}$/){#controllo che la password di conferma contenga almeno 6 caratteri con spazi non ammessi
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>Conferma password</strong> deve contenere almeno 6 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            if($password ne $password_confirm){#controllo che le password coincidano
                $error=$error."\t\t\t<li>Le password non coincidono.</li>\n";
                $correct_input=0;
            }
            $error=$error."\t\t</ul>\n";
            if($correct_input==1){
                $error=undef; # ripulisco $error
            }
        }
        if($correct_input==1){
            my $parser = XML::LibXML->new();
            my $doc=$parser->parse_file('../public_html/xml/users.xml');
            my $root = $doc->getDocumentElement;
            my @users=$root->findnodes("//utente[username='$username']");
            if(@users){
                $error="\t\t\t<p>Username gi&agrave; in uso.</p>";
                &print_registration($error,$nome,$cognome,$mail,$telefono,$username);
            }
            else{
                my $password=md5_hex($password);
                $elem = "
    <utente>
        <nome>$nome</nome>
        <cognome>$cognome</cognome>
        <email>$mail</email>
        <telefono>$telefono</telefono>
        <username>$username</username>
        <password>$password</password>
        <tipo>base</tipo>
        <commenti>
            <commento>
                <testo/>
                <valutazione/>
            </commento>
        </commenti>
    </utente>
                ";
                $framm = $parser->parse_balanced_chunk($elem);
                $root->appendChild($framm);

                print OUT $doc->toString;
                $doc->toFile('../public_html/xml/users.xml');

                my $session=CGI::Session->new();
                my $cookie=$cgi->cookie(-name=>$session->name,
                                        -value=>$session->id);
                my $cookie_user=$cgi->cookie(-name=>'username',
                                        -value=>$session->param('username'));
                print $cgi->header(-cookie=>[$cookie,$cookie_user]);
                $session->param('username',$username);
                $session->param('password',$password);
                $session->expire('+20m'); # scadenza della sessione = 20 minuti
                &print_confirm($nome,$cognome,$mail,$telefono,$username,'registration');
            }
        }
        else{
            &print_registration($error,$nome,$cognome,$mail,$telefono,$username);
        }
    }
}
