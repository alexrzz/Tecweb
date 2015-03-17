#!/usr/bin/perl
require 'library.pl';

use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use Encode;

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

$id=$cgi->param('domanda');
$scelta=$cgi->param('submit');
$risp=$cgi->param('risp');
$javascript=$cgi->param('javascript');

	&start_page("Rispondi alle domande - Aynwed - Assistenza Tecnica Informatica","Pagina dedicata alla risposta da parte di un esperto",
    			"","conferma_risposta.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"restricted.cgi\">Area Riservata</a> >> Conferma Risposta");
    &print_nav("conferma_risposta.cgi");
    &start_content();

    $parser = XML::LibXML->new();
    $doc=$parser->parse_file('../public_html/xml/chiedi.xml');
    $root = $doc->getDocumentElement;
    

    my @question=$root->findnodes("//domanda[id='$id']");
    
    if(!defined($risp))
    {$correct_input=0;}
    else {$correct_input=1;}
    
    if(!defined($scelta)){#prima invocazione della pagina
    	    print "<h3>Domanda selezionata.</h3>";

    print <<HTML;

    <form action="conferma_risposta.cgi" method="post" id="rispondi">
    <fieldset>

HTML

    print "$error";
    print "\n\t\t<div class=\"domande_admin\">\n ";
    foreach $dom(@question){
    	$user = $dom->findnodes("utente/text()");
    	$testo = $dom->findnodes("testo/text()");

        $user = encode('utf-8',$user);
        $testo = encode('utf-8',$testo);

        print <<HTML;

        <p>
            $user : $testo
        </p>
        <label for="risp">Risposta: </label>
        <textarea rows="5" cols="5" name="risp" id="risp">$risp</textarea>
HTML
    }
    print "\n\t\t</div>";

    print <<HTML;
  
    <noscript>
        <fieldset class="script">
            <input type="hidden" id="javascript" name="javascript" value="false"/>
        </fieldset>
    </noscript>
  
    <input type="hidden" name="domanda" value="$id"/>
    <input type="submit" value="Rispondi" name="submit" onclick="return checkAddAnswer()"/>
    <input type="submit" value="Rifiuta domanda" name="submit"/>
    </fieldset>
    </form>

HTML
    }
else{ #premuto pulsante di invio form
  $domanda = $doc->findnodes("//domanda[id='$id']")->get_node(1);
  
  if($scelta eq "Rispondi")#Selezionata opzione di risposta per la domanda
  {
    #controlli sull'input
    my $error;
        #controllo sull'input nel caso in cui javascript sia disabilitato
        if(defined($javascript)){
            $error="\t\t<ul id=\"ul_riserv\">\n";

            if($risp eq "" || !defined($risp)){#controllo se inserita risposta
                $error=$error."\t\t\t<li>Il campo <strong>Risposta</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($risp!~/^([^!@#^&*]+)$/){#verifico che la riposta non contenga caratteri speciali
                $error=$error."\t\t\t<li>Il campo <strong>Risposta</strong> contiene un carattere non ammesso (!@#$%^&*)</li>\n";
                $correct_input=0;
            }
            $error=$error."\t\t</ul>\n";
            if($correct_input==1){
                $error=undef; # ripulisco $error
            }
        }
        if($correct_input==1){  
	    #inserisco la nuova risposta
	    $elem="	<risposta>$risp</risposta>
	    ";
	    
	    $framm = $parser->parse_balanced_chunk($elem);
	    $domanda->appendChild($framm);
	    print OUT $doc->toString;
	    $doc->toFile('../public_html/xml/chiedi.xml');
	    
	    print "<p>Risposta pubblicata correttamente.</p>";
	}
	else{
	    print "<h3>Domanda selezionata.</h3>";

    print <<HTML;

    <form action="conferma_risposta.cgi" method="post" id="rispondi">

HTML

    print "$error";
    print "\n\t\t<div class=\"domande_admin\">\n ";
    foreach $dom(@question){
    	$user = $dom->findnodes("utente/text()");
    	$testo = $dom->findnodes("testo/text()");
        print <<HTML;

        <p>
            $user : $testo
        </p>
        <label for="risp">Risposta: </label>
        <textarea rows="5" cols="5" name="risp">$risp</textarea>
HTML
    }
    print "\n\t\t</div>";

    print <<HTML;
  
    <noscript>
        <fieldset class="script">
            <input type="hidden" id="javascript" name="javascript" value="false"/>
        </fieldset>
    </noscript>
  
    <input type="hidden" name="domanda" value="$id">

    <div id="submitBtn">
        <input type="submit" value="Rispondi" name="submit" onClick="return checkAddAnswer()"/>
        <input type="submit" value="Rifiuta domanda" name="submit">
    </div>
    
    </form>

HTML
	}
  }
  else #si e' scelto di scartare la domanda
  {
     $node = $doc->findnodes("//domanda[id='$id']/id/text()")->get_node(1);
     $domanda->removeChild($node);
     
     $node = $doc->findnodes("//domanda[id='$id']/utente/text()")->get_node(1);
     $domanda->removeChild($node);
     
     $node = $doc->findnodes("//domanda[id='$id']/testo/text()")->get_node(1);
     $domanda->removeChild($node);
    
     $parent = $domanda->parentNode;
     $parent->removeChild($domanda);
     
    print OUT $doc->toString;
    $doc->toFile('../public_html/xml/chiedi.xml');
     
     print "<p>Domanda rimossa correttamente.</p>";
  }
}


    &end_content();
	&print_footer();
	&end_page();
}
