#!/usr/bin/perl
##-----------------------------------------------------------------##
##                                                                 ##
##                                                                 ##
## © Copyright Mr Lyle R Hopkins 2005. All rights reserved. No part##
## of this or any of the attached documents shall be               ##
## reproduced/stored in any way whatsoever without written         ##
## permission from the Copyright holder.                           ##
##   The Copyright holder holds no responsibility for errors or    ##
## omissions. No liability is assumed in any way for damages       ##
## resulting from the use of this document/program.                ##
##                                                                 ##
## Have a nice day.                                                ##
##                                                                 ##
##                                                                 ##
##-----------------------------------------------------------------##

## By Lyle Hopkins ##


##################################################
######################## Define variables
##################################################

$|=1;

## Choose operating system

BEGIN {
  if (($^O eq 'MSWin32') || defined($ENV{'OS'})) {
    $operatingsystem = 0;
    $operatingsystemoldnt = 0;
    $systempath = "$ENV{'PATH_TRANSLATED'}";
    $systempath =~ s/(\\[a-z\_\-0-9]*\.cgi)$//g;
    $systempath =~ s/(\\[a-z\_\-0-9]*\.pl)$//g;
    unless ($systempath) {
      $systempath = "$ENV{'SCRIPT_FILENAME'}";
      $systempath =~ s/(\\[a-z\_\-0-9]*\.cgi)$//g;
      $systempath =~ s/(\\[a-z\_\-0-9]*\.pl)$//g;
    } ## End unless
#    $operatingsystemoldnt = 1;
#    $slash = '\\';
    $slash = '/';
  } ## End if
  else {
    $operatingsystem = 1;
    $systempath = "$ENV{'SCRIPT_FILENAME'}";
    $systempath =~ s/(\/[a-z0-9\_\-]*\.cgi)$//g;
    $systempath =~ s/(\/[a-z0-9\_\-]*\.pl)$//g;
    if ($systempath =~ /cgiwrap/) {
      $systempath = "$ENV{'PATH_TRANSLATED'}";
      $systempath =~ s/(\/[a-z\_\-0-9]*\.cgi)$//g;
      $systempath =~ s/(\/[a-z\_\-0-9]*\.pl)$//g;
    } ## End if
    $slash = '/';
  } ## End else
###$systempath = "system path to your folder"; ## Enter the correct value and un-comment this if you are having system path detection problems
  push (@INC, "$systempath");
} ## End BEGIN

use cosmic;


##################################################
######################## Other variables
##################################################

my %WHATWANT = &CommonSub::get_get_data;


##################################################
################### Get Cookie
##################################################

my $userhandle = &CommonSub::GetAnyCookie("AFFILIATE");

my $pathtoaffiliate2 = $WHATWANT{'programurl'} . "/affiliate2.cgi?want=click2";

my $query = "affiliate=$userhandle&id=$WHATWANT{'id'}&amount=$WHATWANT{'amount'}&site=$WHATWANT{'site'}&enc=$WHATWANT{'enc'}";
use LWP::UserAgent;
my $ua = new LWP::UserAgent;
my $req = new HTTP::Request 'POST',"$pathtoaffiliate2";
$req->content_type('application/x-www-form-urlencoded');
$req->content($query);
my $res = $ua->request($req);


print "Content-type:text/html\n\n";


