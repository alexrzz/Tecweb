#!/usr/bin/perl
use Digest::MD5 qw(md5_hex);

print "Content-type: text/html\n\n";

$password = "tecweb";
print "Prima -> ".$password;
$password=md5_hex($password);
print "\n Dopo -> ".$password;
