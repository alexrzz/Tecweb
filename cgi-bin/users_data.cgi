#!/usr/bin/perl

require 'library.pl';

use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use Digest::MD5 qw(md5_hex);

$session=CGI::Session->load();
if($session->is_expired && $session->is_empty){
    # utente non autenticato
    print "Location: login.cgi\n\n";
}
else{
    my $cgi=new CGI;
    #recupero parametri inserti dall'utente
    $username=$session->param('username');
    my $javascript=$cgi->param('javascript');

    #recupero parametri da file xml
    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/users.xml');
    $root = $doc->getDocumentElement;

    #recupero parametri inserti dall'utente
    $nome=$cgi->param('nome');
    $cognome=$cgi->param('cognome');
    $mail=$cgi->param('mail');
    $telefono=$cgi->param('telefono');
    $javascript=$cgi->param('javascript');

    if(!defined($nome) and !defined($cognome) and !defined($mail) and !defined($telefono)){
        #prima invocazione della pagina...stampo i dati recuperati dal file xml
        $nome = $doc->findnodes("//utente[username='$username']/nome/text()");
        $cognome = $doc->findnodes("//utente[username='$username']/cognome/text()");
        $mail = $doc->findnodes("//utente[username='$username']/email/text()");
        $telefono = $doc->findnodes("//utente[username='$username']/telefono/text()");

        $correct_input=0;
    }
    else{
        $correct_input=1;
    }
    
        my $error;
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
            $error=$error."\t\t</ul>\n";
            if($correct_input==1){
                $error=undef; # ripulisco $error
            }
        }
        if($correct_input==1){

                my $nd_nome = $doc->findnodes("//utente[username='$username']/nome/text()")->get_node(1);
                my $nd_cognome = $doc->findnodes("//utente[username='$username']/cognome/text()")->get_node(1);
                my $nd_mail = $doc->findnodes("//utente[username='$username']/email/text()")->get_node(1);
                my $nd_telefono = $doc->findnodes("//utente[username='$username']/telefono/text()")->get_node(1);


                $nd_nome->setData($nome);
                $nd_cognome->setData($cognome);
                $nd_mail->setData($mail);
                $nd_telefono->setData($telefono);

                print OUT $doc->toString;
                $doc->toFile('../public_html/xml/users.xml');

                &print_confirm($nome,$cognome,$mail,$telefono,$username,'edit');
        }
        else{
            &print_users_data($error,$nome,$cognome,$mail,$telefono,$username);
        }
}
