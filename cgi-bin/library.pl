#!/usr/bin/perl

#Library per la stampa di html

sub start_page
{

		$title = $_[0];
		$description = $_[1];
		$keywords = $_[2];
		$page_from = $_[3];

		print "Content-type: text/html\n\n";
		print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
	
<head>
<title>$title</title>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<meta name="title" content="$title" />
<meta name="description" content="$description" />
<meta name="keywords" content="$keywords" />
<meta name="author" content="Alex Ruzzante,Federico Vegro, Giacomo Vanin" /> 
<meta name="language" content="italian it" />

<link rel="stylesheet" href="../style/stile.css" type="text/css" media="screen"/>
<link type="text/css" rel="stylesheet" href="../style/base.css" media="handheld, screen" />
<link type="text/css" rel="stylesheet" href="../style/small.css" media="handheld, screen and (max-width:680px), only screen and (max-device-width:680px)" />
<link type="text/css" rel="stylesheet" href="../style/print.css" media="print" />
<link type="text/css" rel="stylesheet" href="../style/aural.css" media="aural" />

<script type="text/javascript" src="../js/script.js"></script>

<link rel="icon" href="../img/favicon.ico" type="image/x-icon" />
<link rel="alternate" type="application/rss+xml" title="" href="" />
</head>

<body>
HTML
}

sub print_header{

	print<<HTML;
<div id="header">
	<img src="../img/logo.png" id="headImg" alt="logo Azienda" />
	
	<div id="headerText">
		<div id="headerUtility">
HTML

if(!($page_from eq "restricted.cgi")){
print <<HTML;
	<a href="restricted.cgi">Area Riservata</a>
HTML
}
else{
print <<HTML;
	<a href="logout.cgi">Logout</a>
HTML
}





print <<HTML;
			<a href="register.cgi" title="Registrazione nuovo utente">Registrazione</a>

			<span class="aural">
				<a href="#content">Vai ai contenuti</a>
			</span>
		</div>
			
	<h1 class="auralNotRead">All You Need WE Do</h1>
	<h2>Servizi di riparazione ed assistenza tecnica informatica per privati ed aziende</h2>
		
	</div>
</div>
HTML
}

sub print_breadcrumb{
	$path = $_[0];
print <<HTML;
	<div id="breadcrumb">
		Ti trovi in: $path
	</div>
HTML
}

sub print_nav{
print <<HTML;
	<div id="nav">
		<ul>
			<li><a tabindex="1" href="../index.html" class= "blocco"><span xml:lang="en">Home</span></a></li>
			<li><a tabindex="2" href="../privati.html" class= "blocco">Privati</a></li>
			<li><a tabindex="3" href="../business.html" class= "blocco"><span xml:lang="en">Business</span></a></li>
			<li><a tabindex="4" href="../chisiamo.html" class= "blocco">Chi siamo</a></li>
			<li><a tabindex="5" href="../contatti.html" class= "blocco">Contatti</a></li>
HTML
			if($_[0] eq "chiedi.cgi"){
				print "<li id=\"active\">Chiedi all'esperto</li>";
			}
			else{
				print "<li><a href=\"chiedi.cgi\" class= \"blocco\">Chiedi all'esperto</a></li>";
			}
print <<HTML;
			
		</ul>
	</div>
HTML
}

sub start_content{
	print "<div id=\"content\">";
}

sub end_content{
	print "</div>";
}

sub print_footer{
	print <<HTML;
	<div id="footer">
        <img src="../img/css.png" class="valid" alt="CSS Valid!"/>
        <img src="../img/xhtml.png" class="valid" alt="XHTML 1.0 Valid!"/>
        <strong>2014 Aynwed S.P.A.</strong> Via Trieste, 63, 35121 Padova, P.IVA 01234567899
    </div>
HTML
}


sub end_page{
	print <<EOF;
</body>
</html>

EOF
}

sub print_login{
	&start_page("Login - Aynwed - Assistenza tecnica informatica","Pagina di autenticazione al sito",
    			"utente,login","login.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Login");
    &print_nav();
    &start_content();


	#stampo eventuali errori
	if(defined($_[1])){
        print $_[1];
    }
print <<HTML;
        <form action="login.cgi" method="post" id="login">
            <fieldset>
                <legend>Dati utente</legend>
                <label for="username">Nome utente</label>
                <input id="username" name="username" value=""/>
                <label for="password">Password</label>
                <input type="password" id="password" name="password"  value=""/>
                <input type="hidden" id="source" name="source" value="$_[0]" readonly="readonly" />

                <div>
	                <input type="reset" value="Cancella tutto" />
	                <input type="submit" value="Accedi" onclick="return checkLogin()" />
            	</div>

            </fieldset>
            <noscript>
            <fieldset class="script">
                <input type="hidden" id="javascript" name="javascript" value="false"/>
            </fieldset>
            </noscript>
        </form>
        <p>
            <a href="register.cgi" title="Registrazione">Non hai un account? Registrati qui.</a>
        </p>
HTML

&end_content();
&print_footer();
&end_page();
}

sub print_registration{

	
	&start_page("Registrazione - Aynwed - Assistenza tecnica informatica","Pagina di registrazione di un nuovo utente",
    			"utente,registrazione","new_user.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Registrazione");
    &print_nav();
    &start_content();

	print "<h3>Registrazione nuovo utente</h3>";

	#stampo eventuali errori
	print $_[0];

	#stampo form html
	print <<HTML;		
		<form id="registrazione" action="register.cgi" method="post">
			<fieldset>
				<legend>Informazioni personali</legend>
				
				<label for="nome">Nome:</label>
				<input type="text" id="nome" name="nome" value="$_[1]"/>
				
				<label for="cognome">Cognome:</label>
				<input type="text" id="cognome" name="cognome" value="$_[2]"/>
				
				<label for="mail" xml:lang="en">Mail:</label>
				<input type="text" id="mail" name="mail" value="$_[3]"/>
				
				<label for="telefono">Telefono:</label>
				<input type="text" id="telefono" name="telefono" value="$_[4]" size="10" maxlength="10"/>
			</fieldset>

			<fieldset>
				<legend>Dati utente</legend>
				<label for="username">Nome utente:</label>
				<input type="text" id="username" name="username" value="$_[5]"/>
				
				<label for="password" xml:lang="en">Password:</label>
				<input type="password" id="password" name="password"/>
				
				<label for="repass">Conferma <span xml:lang="en">password</span>:</label>
				<input type="password" id="repass" name="repass"/>
			</fieldset>

			<div id="submitBtn">
				<input type="reset" name="resetReg" id="resetReg" value="Cancella Campi"/>
				<input type="submit" name="submitReg" id="submitReg" value="Registrati" onclick="return checkRegistration()"/>
			</div>

			<noscript>
	            <fieldset class="script">
	                <input type="hidden" id="javascript" name="javascript" value="false"/>
	            </fieldset>
            </noscript>

		</form>
HTML

&end_content();
&print_footer();
&end_page();
}

sub print_users_data{
		&start_page("Dati utente - Aynwed - Assistenza tecnica informatica","Pagina di modifica dei dati utente",
    			"utente","users_data.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"restricted.cgi\">Area Riservata</a> >> Modifica dati utente");
    &print_nav();
    &start_content();

	#stampo eventuali errori
	print $_[0];

	#stampo form html
	print <<HTML;		
		<form id="edit_user" action="users_data.cgi" method="post">
			<fieldset>
				<legend>Informazioni personali</legend>
				
				<label for="nome">Nome:</label>
				<input type="text" id="nome" name="nome" value="$_[1]"/>
				
				<label for="cognome">Cognome:</label>
				<input type="text" id="cognome" name="cognome" value="$_[2]"/>
				
				<label for="mail" xml:lang="en">Mail:</label>
				<input type="text" id="mail" name="mail" value="$_[3]"/>
				
				<label for="telefono">Telefono:</label>
				<input type="text" id="telefono" name="telefono" value="$_[4]" size="10" maxlength="10"/>
			</fieldset>

			<fieldset>
				<legend>Dati utente</legend>
				<p>Nome utente: <strong>$_[5]</strong></p>
			</fieldset>
			
			<div id="submitBtn">
				<input type="submit" name="submitEdit" id="submitEdit" value="Modifica" onclick="return checkEditUser()"/>
			</div>

			<noscript>
	            <fieldset class="script">
	                <input type="hidden" id="javascript" name="javascript" value="false"/>
	            </fieldset>
            </noscript>

		</form>
HTML

&end_content();
&print_footer();
&end_page();
}

sub print_confirm{

    if($_[5] eq "registration"){
		&start_page("Conferma Registrazione - Aynwed - Assistenza tecnica informatica","Pagina di conferma",
    			"utente,conferma,registrazione","register.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata
	}
	else{
		&start_page("Conferma modifica dati utente - Aynwed - Assistenza tecnica informatica","Pagina di conferma",
    			"utente,conferma,modifica","users_data.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata	
	}

    &print_header();
    if($_[5] eq "registration"){
    	&print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Conferma Registrazione");
	}
	else{
		&print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> <a href=\"restricted.cgi\">Area Riservata</a> >> Conferma modifica dati utente");	
	}
    &print_nav();
    &start_content();

    if($_[5] eq "registration"){
    	print "<h3>Registrazione effettuata con successo!</h3>";
    }
    else{
    	print "<h3>Modifica effettuata con successo!</h3>";
    }

    print "<p>I tuoi dati: </p>";

    print <<HTML;

<ul id="ul_riserv">
	<li><strong>Nome: </strong>$_[0]</li>
	<li><strong>Cognome: </strong>$_[1]</li>
	<li><strong>Mail: </strong>$_[2]</li>
	<li><strong>Telefono: </strong>$_[3]</li>
	<li><strong>Username: </strong>$_[4]</li>
</ul>

HTML

	&end_content();
	&print_footer();
	&end_page();

}

sub logged_user{
	&start_page("Registrazione - Aynwed - Assistenza tecnica informatica","Pagina di registrazione di un nuovo utente",
    			"utente,registrazione","restricted.cgi");#parametri: Titolo, Descrizione, Keywords, pagina chiamata

    &print_header();
    &print_breadcrumb("<a href=\"../index.html\"><span xml:lang=\"en\">Home</span></a> >> Registrazione");
    &print_nav();
    &start_content();

    print <<HTML;
    <h3>Utente $_[0] già autenticato.</h3>
    <p>
	    <ul id="ul_riserv">
	    	<li><a href="restricted.cgi">Vai all'area riservata.</a></li>
			<li><a href="logout.cgi">LOGOUT.</a></li>
		</ul>
	</p>
HTML

    &end_content();
    &print_footer();
	&end_page();
}

sub redirect{
    print "Content-type: text/html\n\n";
    # codice XHTML della pagina
print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
HTML
        print "\t\t<meta http-equiv='refresh' content='0;url=restricted.cgi' />\n";
print <<HTML;
</head>
<body>
<body />
</html>
HTML
}


#sub getSession{
#	$session = CGI::Session->load() or die $!;
#	if($session->is_expired || $session->is_empty)
#	{
#		return undef;
#	}
#	else{
#		my $utente = $session->param('utente');
#		return $utente;
#	}
#}

#sub destroySession{
#	$session = CGI::Session->load() or die $!;
#	$SID = $session->id();
#	$session->close();
#	$session->delete();
#	$session->flush();
#}

#sub createSession{#parametro nome utente
#	$nome_utente = $_[0];
#	$session = new CGI::Session();
#	$session->param('utente', $nome_utente);
#	$session->expire('+20m');
#}

1;