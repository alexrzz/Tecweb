#!/usr/bin/perl
require 'library.pl';

use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use Encode;

# (1) VERIFICA AUTENTICAZIONE UTENTE
# Verifico se l'utente è autenticato (in caso contrario, redireziono alla pagina
# di login).
$session=CGI::Session->load();
$cgi = new CGI;

	&start_page("Chiedi All'Esperto - Aynwed - Assistenza Tecnica Informatica","Pagina con domande da parte degli utenti e risposte di un nostro esperto",
    			"chiedi,esperto,faq","chiedi.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Chiedi all'esperto");
    &print_nav("chiedi.cgi");
    &start_content();

    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/chiedi.xml');
    $root = $doc->getDocumentElement;
    

    my @questions=$root->findnodes("//domanda");

    print "<h3>Domande degli utenti e risposte del nostro esperto.</h3>";
    print "<p><a href=\"insert_question.cgi\">Inserisci la tua domanda.</a></p>";

    print "\n\t\t<div class=\"domande\">";
    foreach $domanda(@questions){
    	$user = $domanda->findnodes("utente/text()");
    	$testo = $domanda->findnodes("testo/text()");
    	$risposta = $domanda->findvalue("risposta/text()");

        $user = encode('utf-8',$user);
        $testo = encode('utf-8',$testo);
        $risposta = encode('utf-8',$risposta);

    	if($risposta ne ""){
    		print <<HTML;

    		<dl>
    			<dt>$user: $testo</dt>
    			<dd>$risposta</dd>
    		</dl>
HTML
    	}
    }
    print "\n\t\t</div>";




    &end_content();
	&print_footer();
	&end_page();
