<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:a="http://www.aynwed.com" exclude-result-prefixes="a">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'
doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

<xsl:template match="/" >
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
<head>
<title>Le News - Aynwed - Assistenza tecnica informatica</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

<meta name="title" content="News - Aynwed - Assistenza tecnica informatica" />
<meta name="description" content="Tutte le news del sito di Aynwed" />
<meta name="keywords" content="Riparazione, assistenza, tecnica, informatica, corsi, formazione" />
<meta name="author" content="Alex Ruzzante, Federico Vegro, Giacomo Vanin" /> 
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
	<div id="header">
		<img src="../img/logo.png" id="headImg" alt="logo Azienda" />
	
		<div id="headerText">
			<div id="headerUtility">
			
				<a href="../cgi-bin/restricted.cgi">Area Riservata</a>
				<a href="../cgi-bin/register.cgi" title="Registrazione nuovo utente">Registrazione</a>

				<span class="aural">
					<a href="#content">Vai ai contenuti</a>
				</span>
			</div>
			
		<h1 class="auralNotRead">All You Need WE Do</h1>
		<h2>Servizi di riparazione ed assistenza tecnica informatica per privati ed aziende</h2>
		
		</div>
	</div>
	
	<div id="breadcrumb">
		Ti trovi in: <a href="../index.html"><span xml:lang="en">Home</span></a> >> <span xml:lang="en">News</span>
	</div>
	
	<div id="nav">
		<ul>
			<li><a href="../index.html" class= "blocco"><span xml:lang="en">Home</span></a></li>
			<li><a href="../privati.html" class= "blocco">Privati</a></li>
			<li><a href="../business.html" class= "blocco"><span xml:lang="en">Business</span></a></li>
			<li><a href="../chisiamo.html" class= "blocco">Chi siamo</a></li>
			<li><a href="../contatti.html" class= "blocco">Contatti</a></li>
			<li><a href="../cgi-bin/chiedi.cgi" class= "blocco">Chiedi all'esperto</a></li>
		</ul>
	</div>
	
	<div id="content">
		<div id="notizie">
		    <xsl:for-each select="a:notizie/a:notizia">
		    <xsl:sort select="position()" data-type="number" order="descending"/>
			<dl>
			  <dt xml:space="preserve">
				  <xsl:value-of select="a:data"/> - 
				  <xsl:value-of select="a:titolo"/> - 
				  <xsl:value-of select="a:categoria"/>
				  </dt>
			  <dd xml:space="preserve">
				  <xsl:value-of select="a:descrizione"/>
			  </dd>
			</dl>
		    </xsl:for-each>
	 	</div>
	</div>
	
	<div id="footer">
		<img src="../img/css.png" class="valid" alt="CSS Valid!"/>
		<img src="../img/xhtml.png" class="valid" alt="XHTML 1.0 Valid!"/>
		<strong>2014 Aynwed S.P.A.</strong> Via Trieste, 63, 35121 Padova, P.IVA 01234567899
	</div>
</body>
</html>
</xsl:template> 
        
</xsl:stylesheet>
