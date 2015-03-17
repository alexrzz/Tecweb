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

if($session->is_expired || $session->is_empty){
    # utente non autenticato
    print "Location: login.cgi\n\n";
}
else{

    $utente = $session->param('username');
    if($utente ne 'admin'){
      # utente semplice respinto
      print "Location: restricted.cgi\n\n";
    }

	&start_page("Rispondi alle domande - Aynwed - Assistenza Tecnica Informatica","Pagina dedicata alla risposta da parte di un esperto",
    			"","rispondi.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"restricted.cgi\">Area Riservata</a> >> Rispondi");
    &print_nav("rispondi.cgi");
    &start_content();

    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/chiedi.xml');
    $root = $doc->getDocumentElement;

    my @questions=$root->findnodes("//domanda");
    
    $count = 0;

    print "<h3>Tutte le domande in sospeso.</h3>";

    print "\n\t\t<div class=\"domande_admin\">\n ";
    foreach $domanda(@questions){
        $id = $domanda->findvalue("id/text()");
    	$user = $domanda->findnodes("utente/text()");
    	$testo = $domanda->findnodes("testo/text()");
        $risposta = $domanda->findvalue("risposta/text()");

        $user = encode('utf-8',$user);
        $testo = encode('utf-8',$testo);

    	if($risposta eq ""){
    		print <<HTML;
                <form action="conferma_risposta.cgi" method="post" id="rispondi">
                <fieldset>
    			<p><input type="radio" value="$id" name="domanda" checked="checked"  /> $user: $testo</p>
HTML
		$count = $count + 1;
    	}
    }
    print "\n\t\t</div>";

    if($count ne 0){
    print <<HTML;
    <input type="submit" value="Seleziona" />
    </fieldset>
    </form>

HTML
}
else
{
  print "<p>Nessuna nuova domanda.</p>";
}

    &end_content();
	&print_footer();
	&end_page();
}