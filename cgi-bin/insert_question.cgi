#!/usr/bin/perl

require 'library.pl';

use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use Digest::MD5 qw(md5_hex);

$session=CGI::Session->load();
$utente = "Anonimo";
if(!$session->is_expired && !$session->is_empty){
    # utente autenticato
    $utente = $session->param('username');
}

&start_page("Fai la tua domanda - Aynwed - Assistenza Tecnica Informatica","Pagina con domande da parte degli utenti e risposte di un nostro esperto",
    			"chiedi,esperto,faq","insert_question.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

&print_header();
&print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"chiedi.cgi\">Chiedi all'esperto</a> >> Inserimento domanda");
&print_nav();
&start_content();

    my $cgi=new CGI;
    #recupero parametri inserti dall'utente
    $domanda=$cgi->param('domanda');
    $javascript=$cgi->param('javascript');

    #recupero parametri da file xml
    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/chiedi.xml');
    $root = $doc->getDocumentElement;
    
    if(!defined($domanda))
    {$correct_input=0;}
    else {$correct_input=1;}
    
        my $error;
        #controllo sull'input nel caso in cui javascript sia disabilitato
        if(defined($javascript)){
            $error="\t\t<ul id=\"ul_riserv\">\n";

            if($domanda eq "" || !defined($domanda)){#controllo se inserito campo domanda
                $error=$error."\t\t\t<li>Il campo <strong>Domanda</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($domanda!~/^([^!@#^&*]+)$/){#controllo che la domanda non contenga caratteri speciali
                $error=$error."\t\t\t<li>Il campo <strong>Domanda</strong> contiene un carattere non ammesso (!@#$%^&*)</li>\n";
                $correct_input=0;
            }
            $error=$error."\t\t</ul>\n";
            if($correct_input==1){
                $error=undef; # ripulisco $error
            }
        }
        if($correct_input==1){

		      my $id=$root->findvalue("//domanda[last()]/id/text()");

   	$id = $id + 1;

    $elem="
	<domanda>
		<id>$id</id>
		<utente>$utente</utente>
		<testo>$domanda</testo>
	</domanda>
    ";

    $framm = $parser->parse_balanced_chunk($elem);
    $root->appendChild($framm);

    print OUT $doc->toString;
    $doc->toFile('../public_html/xml/chiedi.xml');

                print <<HTML
	<h3>Domanda inviata con successo!</h3>
	<p>La domanda è stata inoltrata al nostro esperto. Se verrà ritenuta eticamente corretta verrà pubblicata nel più breve
		tempo possibile con la relativa risposta.</p>


HTML
        }
        else{
	print "$error";
	
	print <<HTML;

	<form id="chiedi" action="insert_question.cgi" method="post">
		<p>Utente: $utente</p>
	<fieldset>
	<legend>Domanda</legend>
	<label for="domanda">Domanda:</label>
	<textarea name="domanda" id="domanda" rows="5" cols="50"></textarea>
    <input type="reset" name="resetReg" id="resetReg" value="Cancella Campi"/>
    <input type="submit" name="subChiedi" id="subChiedi" value="Invia" onclick="return checkQuestion()"/>
	</fieldset>

	<noscript>
        <fieldset class="script">
            <input type="hidden" id="javascript" name="javascript" value="false"/>
        </fieldset>
    </noscript>
	</form>
HTML
        }
        
&end_content();
&print_footer();
&end_page();
