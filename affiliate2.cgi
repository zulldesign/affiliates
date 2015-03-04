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

unless ($operatingsystem) {
  use sendmail;
  print "P3P: policyref=\"$policyurl\", CP=\"NOI DSP COR ADMa DEVa TAIa OUR BUS IND UNI COM NAV INT\"\r\n";
} ## End unless
else {
  print "P3P: policyref=\"$policyurl\", CP=\"NOI DSP COR ADMa DEVa TAIa OUR BUS IND UNI COM NAV INT\"\n";
} ## End else

use cosmic;

$variablesfilename = "variables.var";
require $variablesfilename;


##################################################
######################## Other variables
##################################################

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$month = ($mon + 1);
$month = sprintf("%02d", $month);
$mday = sprintf("%02d", $mday);
$year += 1900;
$date = "$year$month$mday";
$time = sprintf("%02d:%02d:%02d", $hour,$min,$sec);
@months = ("January","February","March","April","May","June","July","August","September","October","November","December");
@days = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
## Clean date and time
$thstrder = "th";
if ($mday == 1) { $thstrder = "st"; } ## End if
if ($mday == 2) { $thstrder = "nd"; } ## End if
if ($mday == 3) { $thstrder = "rd"; } ## End if
$datewords = "$days[$wday] $mday$thstrder $months[$mon]";
chomp($w3cdate);
chomp($time);

my %WHATWANT = &CommonSub::get_get_data;
my %FORM = &CommonSub::get_post_data;


##################################################
################### Get Cookie
##################################################

my $userhandle = &CommonSub::GetAnyCookie("AFFILIATE");

my $ordid = $WHATWANT{'id'};
my $ordamount = $WHATWANT{'amount'};
my $passsent = $WHATWANT{'enc'};
if ($poststyle) {
  $ordid = $FORM{$postid};
  $ordamount = $FORM{$postprice};
  if ($postsent) {
    $passsent = $FORM{$postsent};
  } ## End if
} ## End if POST

if ($WHATWANT{'click2'}) {
  $userhandle = $FORM{'affiliate'};
  $ordid = $FORM{'id'};
  $ordamount = $FORM{'amount'};
  $passsent = $FORM{'enc'};
} ## End if

my $clickdata = "$userhandle$months[$mon]$year";

if ($saletrackpassword) {
  unless ($passsent eq $saletrackpassword) {
    my $filename = "error.log";
    &CommonSub::AppendToFile("$systempath$slash$filename","ORDER TRACKING ERROR - Tracking password does not match '$passsent' - ID$ordid AM$ordamount AF$userhandle\n");
    print "Content-type:text/html\n\n";
    exit;
  } ## End unless
} ## End if

if (-e "$systempath$slash$data_path$slash$userhandle") {
  open (FILE, "$systempath$slash$data_path$slash$clickdata");
    @idcheck = <FILE>;
  close (FILE);
  $idcheck = join('',@idcheck);
  if ($idcheck !~ /$ordid¦/) {
    open(OUTF,">>$systempath$slash$data_path$slash$clickdata");
      print OUTF
      "$ordid¦$ordamount¦$date\n";
    close(OUTF);
  } ## End if
  else {
    my $filename = "error.log";
    &CommonSub::AppendToFile("$systempath$slash$filename","ORDER TRACKING ERROR - Order ID $ordid already exists - ID$ordid AM$ordamount AF$userhandle\n");
  } ## End else
} ## End if
else {
  my $filename = "error.log";
  &CommonSub::AppendToFile("$systempath$slash$filename","ORDER TRACKING ERROR - username $userhandle does not exist - ID$ordid AM$ordamount AF$userhandle\n");
} ## End else

if ($poststyle) {
  print "Location: $postredirect\n\n";
} ## End if
else {
  print "Content-type:text/html\n\n";
} ## End else  


