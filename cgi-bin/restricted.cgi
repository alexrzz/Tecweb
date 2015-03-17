#!/usr/bin/perl
require 'library.pl';

use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;
use XML::LibXML;

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

    # utente autenticato
    my $username=$session->param('username');
    my $password=$session->param('password');

    my $parser=XML::LibXML->new();
    my $document=$parser->parse_file('../public_html/xml/users.xml');
    my $root=$document->getDocumentElement;
    my @users=$root->findnodes("//utente[username='$username' and tipo='amministratore']");

    #utente base
    if(@users){
        &restricted_admin($username);
    }
    else{
        &restricted_base($username);
    }

}


sub restricted_admin{
    &start_page("Area Riservata - Aynwed - Assistenza tecnica informatica","Area riservata dell'utente registrato al sito",
                "area,riservata,utente","restricted.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Area Riservata");
    &print_nav();
    &start_content();

    #contenuto area riservata
    print "<h3>Benvenuto $_[0] --- Tipo: AMMINISTRATORE</h3>";
    print "<p id=\"p_base\">Azioni disponibili:</p>";

    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/chiedi.xml');
    $root = $doc->getDocumentElement;

    my @questions=$root->findnodes("//domanda");
    $new=0;

        foreach $domanda(@questions){
        $risposta = $domanda->findvalue("risposta/text()");

        if($risposta eq ""){
            $new++;
        }
    }

    print<<HTML;

<ul id="ul_riserv">
    <li><a href="rispondi.cgi">Rispondi alle domande.
HTML

if($new!=0){
    print "(nuove domande:<span id=\"new\"> $new</span>)";
}

print<<HTML;
    </li>
    </a>
    <li><a href="add_news.cgi">Aggiungi una news.</a></li>
</ul>
HTML

    &end_content();
    &print_footer();
    &end_page();

}

sub restricted_base{
    &start_page("Area Riservata - Aynwed - Assistenza tecnica informatica","Area riservata dell'utente registrato al sito",
                "area,riservata,utente","restricted.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Area Riservata");
    &print_nav();
    &start_content();

    #contenuto area riservata
    print <<HTML;

<h3>Benvenuto $_[0] --- Tipo: BASE</h3>
<p id="p_base">Azioni disponibili:</p>
<ul id="ul_riserv">
    <li><a href="users_data.cgi">I miei dati.</a></li>
    <li><a href="view_question.cgi">Visualizza domande effettuate.</a></li>
</ul>

HTML
    &end_content();
    &print_footer();
    &end_page();
}
