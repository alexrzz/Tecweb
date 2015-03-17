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

    $data=$cgi->param('data');
    $titolo=$cgi->param('titolo');
    $categoria=$cgi->param('categoria');
    $descrizione=$cgi->param('descrizione');
    $javascript=$cgi->param('javascript');


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

	&start_page("Aggiungi News - Aynwed - Assistenza Tecnica Informatica","Pagina dedicata all'aggiunta di una nuova news.'",
    			"","add_news.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"restricted.cgi\">Area Riservata</a> >> Aggiungi News");
    &print_nav("add_news.cgi");
    &start_content();
    
    if(!defined($data) && !defined($titolo) && !defined($categoria) && !defined($descrizione))
    {#prima invocazione della pagina
	$correct_input = 0;
    }
    else{
	$correct_input = 1;
    }
    
    my $error;
    if(defined($javascript))
    {
      $error="\t\t<ul id=\"ul_riserv\">\n";
      if($titolo eq "")#controllo se inserito campo titolo
      {
         $error=$error."\t\t\t<li>Il campo <strong>Titolo</strong> &egrave; obbligatorio.</li>\n";
         $correct_input=0;
      }
      if($categoria eq "")#controllo se inserito campo categoria
      {
         $error=$error."\t\t\t<li>Il campo <strong>Categoria</strong> &egrave; obbligatorio.</li>\n";
         $correct_input=0;
      }
      if($descrizione eq "")#controllo se inserito campo descrizione
      {
         $error=$error."\t\t\t<li>Il campo <strong>Descrizione</strong> &egrave; obbligatorio.</li>\n";
         $correct_input=0;
      }
      elsif($domanda!~/^([^!@#^&*]+)$/){#controllo che la domanda non contenga caratteri speciali
                $error=$error."\t\t\t<li>Il campo <strong>Descrizione</strong> contiene un carattere non ammesso (!@#$%^&*)</li>\n";
                $correct_input=0;
      }
      if($data eq "")#controllo se inserito campo data
      {
         $error=$error."\t\t\t<li>Il campo <strong>Data</strong> &egrave; obbligatorio.</li>\n";
         $correct_input=0;
      }
      #i valori di mese anno e giorno vengono splittati in un array
      # values[0] -> Anno
      # values[1] -> Mese
      # values[2] -> Giorno
      my @values = split('-', $data);
      
      if(!defined($data) || $data ne "")
      {
	  if(length(@values[2])!=2 || length(@values[1])!=2 || length(@values[0])!=4)#controllo che la lunghezza dei 3 valori sia corretta
	  {
	    $error=$error."\t\t\t<li>Formato data errato. Inserire nella forma aaaa-mm-gg.</li>\n";
	    $correct_input=0;
	  }
	  else{
	    if(@values[2]>31 || @values[2]<1)#verifico che il valore rappresentante i giorni sia compreso tra 1 e 31 
	    {
	      $error=$error."\t\t\t<li>I giorni nel campo data devono essere compresi tra 1 e 31.</li>\n";
	      $correct_input=0;
	    }
	    if(@values[1]>12 || @values[1]<1)#verifico che il valore rappresentante i mesi sia compreso tra 1 e 12 
	    {
	      $error=$error."\t\t\t<li>I mesi nel campo data devono essere compresi tra 1 e 12.</li>\n";
	      $correct_input=0;
	    }
	  }
      }
      $error=$error."\t\t</ul>\n";
      if($correct_input==1){
	  $error=undef; # ripulisco $error
      }
    }
    if($correct_input==1)
    {
        $parser = XML::LibXML->new();
	$doc=$parser->parse_file('../public_html/xml/notizie.xml');
	$root = $doc->getDocumentElement;
      
	$elem="
	    <notizia>
		    <data>$data</data>
		    <titolo>$titolo</titolo>
		    <categoria>$categoria</categoria>
		    <descrizione>
			    $descrizione
		    </descrizione>
	    </notizia>
	";
	
	$framm = $parser->parse_balanced_chunk($elem);
	$root->appendChild($framm);

	print OUT $doc->toString;
	$doc->toFile('../public_html/xml/notizie.xml');
	
	print "<p>Notizia pubblicata correttamente!</p>";
    }
    else
    {
	print <<HTML;
	
	$error

	<form action="add_news.cgi" method="post" id="add_news">
	
	<fieldset>
	<legend>Dati news</legend>
	
	<label for="categoria">Categoria: </label>
	  <select name="categoria" id="categoria">
	      <option value="">--Seleziona Categoria--</option>
	      <option value="Sconto">Sconto</option>
	      <option value="Evento">Evento</option>
	      <option value="Notizia">Notizia</option>
	  </select>
	  
	<label for="data">Data (aaaa-mm-gg) :</label>
	<input type="text" name="data" id="data" size="10" maxlength="10" value="$data"/>
	
	<label for="titolo">Titolo:</label>
	<input type="text" name="titolo" id="titolo" value="$titolo"/>
	
	
	<label for="descrizione">Descrizione:</label>
	<textarea name="descrizione" id="descrizione" cols="4" rows="4">$descrizione</textarea>
	
	</fieldset>
	
	<noscript>
	  <fieldset class="script">
	      <input type="hidden" id="javascript" name="javascript" value="false"/>
	  </fieldset>
	</noscript>

	<div id="submitBtn">
	<input type="submit" value="Aggiungi News" onclick="return checkAddNews()"/>
	</div>
	</form>
HTML
    }
    
    &end_content();
	&print_footer();
	&end_page();
}
