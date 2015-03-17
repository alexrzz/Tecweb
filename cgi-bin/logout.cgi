#!/usr/bin/perl

# NOME
# logout.cgi

# DESCRIZIONE
# Gestisce il logout dell'utente corrente (e redireziona alla pagina di
# benvenuto).

# QUERY STRING
# nessuna

use CGI::Session;

$session=CGI::Session->load();
if(!$session->is_expired && !$session->is_empty){
    $session->delete();
}
print "Location: ../index.html\n\n";