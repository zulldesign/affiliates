#!/usr/bin/perl
##-----------------------------------------------------------------##
##                                                                 ##
##                                                                 ##
## © Copyright Mr Lyle R Hopkins 2004. All rights reserved. No part##
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

$variablesfilename = "variables.var";
require $variablesfilename;


##################################################
######################## Other variables
##################################################

my %WHATWANT = &CommonSub::get_get_data;

my $commissionperiodsecs = $commissionperiod * 86400;
my @months = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");
my @days = ("Sun","Mon","Tue","Wed","Thu","Fri","Sat");
my ($sec,$min,$hr,$mday,$mon,$yr,$wday,$yday,$isdst) = gmtime(time + $commissionperiodsecs);
my $timestr = sprintf("%3s, %02d-%3s-%4d %02d:%02d:%02d GMT", $days[$wday],$mday,$months[$mon],$yr+1900,$hr,$min,$sec);


if ($WHATWANT{'user'} eq "") {
  print "Location: $site1\n\n";
  exit;
} ## End if

my $userhandle = $WHATWANT{'user'};


##################################################
################### Check user name really exists
##################################################

if (-e "$systempath$slash$data_path$slash$userhandle") {
  if ($WHATWANT{'site'} eq "site1") {
    $siteurl = $site1;
  } ## End if
  elsif ($WHATWANT{'site'} eq "site2") {
    $siteurl = $site2;
  } ## End if
  elsif ($WHATWANT{'site'} eq "site3") {
    $siteurl = $site3;
  } ## End if
  elsif ($WHATWANT{'site'} eq "site4") {
    $siteurl = $site4;
  } ## End if
  elsif ($WHATWANT{'site'} eq "site5") {
    $siteurl = $site5;
  } ## End if
  else {
    $siteurl = $site1;
  } ## End if
} ## End if
else {
  print "Location: $site1\n\n";
  exit;
} ## End else


##################################################
################### Secure Tracking
##################################################

if ($securetracking) {
  unless ($WHATWANT{'s'}) {
    $siteurl = $secureurl . "/click.cgi?user=$WHATWANT{'user'}&site=$WHATWANT{'site'}&period=$commissionperiod&programurl=$programurl&policy=$policyurl";
  } ## End unless
} ## End if


##################################################
################### Set Cookie
##################################################

if ($operatingsystem) {
  print "P3P: policyref=\"$policyurl\", CP=\"NOI DSP COR ADMa DEVa TAIa OUR BUS IND UNI COM NAV INT\"\n";
  print "Set-Cookie: AFFILIATE=$userhandle; path=/; expires=$timestr\n";
  print "Location: $siteurl\n\n";
} ## End if
else {
  if ($operatingsystemoldnt) {
    print "HTTP/1.0 302 Redirect\r\n";
  } ## End if
  print "Location: $siteurl\r\n";
  print "P3P: policyref=\"$policyurl\", CP=\"NOI DSP COR ADMa DEVa TAIa OUR BUS IND UNI COM NAV INT\"\r\n";
  print "Set-Cookie: AFFILIATE=$userhandle; path=/; expires=$timestr\r\n\r\n";
} ## End else

