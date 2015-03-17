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
if($session->is_expired && $session->is_empty){
    # utente non autenticato
    print "Location: login.cgi\n\n";
}
else{
$cgi = new CGI;

	&start_page("Domande utente - Aynwed - Assistenza Tecnica Informatica","Pagina per la visualizzazione delle domande effettuate da un utente registrato",
    			"chiedi,esperto,faq","chiedi.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"restricted.cgi\">Area Riservata</a> >> Domande effettuate");
    &print_nav("view_question.cgi");
    &start_content();

    $utente = $session->param('username');

    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/chiedi.xml');
    $root = $doc->getDocumentElement;
    

    my @questions=$root->findnodes("//domanda[utente='$utente']");

    print "<h3>Domande effettuate da \"$utente\".</h3>";

    print "\n\t\t<div class=\"domande\">";
    foreach $domanda(@questions){
    	$user = $domanda->findnodes("utente/text()");
    	$testo = $domanda->findnodes("testo/text()");
    	$risposta = $domanda->findvalue("risposta/text()");

        $user = encode('utf-8',$user);
        $testo = encode('utf-8',$testo);
        $risposta = encode('utf-8',$risposta);

    		print <<HTML;
    		<dl>
    			<dt>$user: $testo</dt>
HTML
            if($risposta eq ""){
                print "<dd>***Domanda in attesa di approvazione***</dd>";}
            else{
                print "<dd>$risposta</dd>";}
            print <<HTML;
    		</dl>
HTML
    }
    print "\n\t\t</div>";

    &end_content();
	&print_footer();
	&end_page();
}