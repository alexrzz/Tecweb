#!/usr/bin/perl

require 'library.pl';

use CGI;
use CGI::Session;
use XML::LibXML;
use Digest::MD5 qw(md5_hex);

$session=CGI::Session->load();
if(!$session->is_expired && !$session->is_empty){
    # utente autenticato
    print "Location: restricted.cgi\n\n";
}
else{
    # utente non autenticato
    my $cgi=new CGI;
    my $source=$cgi->param('source');
    my $username=$cgi->param('username');
    my $password=$cgi->param('password');
    my $javascript=$cgi->param('javascript');
    if(!defined($username) || !defined($password)){
        # prima invocazione della pagina
        if(!defined($source)){
            $source="restricted.cgi";
        }
        &print_login($source,undef);
    }
    else{
        my $error;
        my $correct_input=1;
        if(defined($javascript)){
            $error="\t\t<ul id=\"ul_riserv\">\n";
            if($username eq ""){#controllo se inserito campo username
                $error=$error."\t\t\t<li>Il campo <strong>username</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($username!~/^\S{3,}$/){#controllo che il campo username contenga almeno 3 caratteri con spazi non ammessi
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>username</strong> deve contenere almeno 3 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            if($password eq ""){#controllo se inserito campo password
                $error=$error."\t\t\t<li>Il campo <strong>password</strong> &egrave; obbligatorio.</li>\n";
                $correct_input=0;
            }elsif($password!~/^\S{6,}$/){#controllo che la password contenga almeno 6 caratteri con spazi non ammessi
                $error=$error."\t\t\t<li>Il valore immesso nel campo <strong>password</strong> deve contenere almeno 6 caratteri (spazi non ammessi).</li>\n";
                $correct_input=0;
            }
            $error=$error."\t\t</ul>\n";
            if($correct_input==1){
                $error=undef; # ripulisco $error
            }
        }
        if($correct_input==1){
            $password=md5_hex($password);
            my $parser=XML::LibXML->new();

            my $document=$parser->parse_file('../public_html/xml/users.xml');
            my $root=$document->getDocumentElement;
            my @users=$root->findnodes("//utente[username='$username' and password='$password']");

            if(@users){
                my $session=CGI::Session->new();
                my $cookie=$cgi->cookie(-name=>$session->name,
                                        -value=>$session->id);
                my $cookie_user=$cgi->cookie(-name=>'username',
                                        -value=>$session->param('username'));
                print $cgi->header(-cookie=>[$cookie,$cookie_user]);
                $session->param('username',$username);
                $session->param('password',$password);
                $session->expire('+20m'); # scadenza della sessione = 20 minuti
                &redirect($source);
            }
            else{
                $error="\t\t<p>Nome utente e password inserite non corrispondono ad alcun utente registrato.</p>";
                &print_login($source,$error);
            }
        }
        else{
            &print_login($source,$error);
        }
    }
}
