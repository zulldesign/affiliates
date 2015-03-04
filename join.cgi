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
} ## End unless

use cosmic;

$variablesfilename = "variables.var";
require $variablesfilename;


##################################################
######################## Show User posted data
##################################################

print "Content-type:text/html\n\n";

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
chomp($date);
chomp($time);

$joinuppage = "joinup.html";
$joinuppage2 = "joinup2.html";

%WHATWANT = &CommonSub::get_get_data();
%FORM = &CommonSub::get_post_data();


##################################################
######################## Check user fields
##################################################

########### Check user name does'nt already exist
my $filename = "$FORM{'username'}";
if (-e "$systempath$slash$data_path$slash$filename") {
  &ErrorHandle::errormessage("The UserName you have selected is already in use$backhtml",0);
} ## End if

foreach $key (keys(%FORM)) {
  my ($valid, $invchar) = &CommonSub::CheckInvalidInput($FORM{'$key'});
  if ($valid) {
    &ErrorHandle::errormessage("$key field contains invalid characters '$invchar'",0);
  } ## End if
} ## End loop

unless (&CommonSub::CheckEmail($FORM{'email'})) { &ErrorHandle::errormessage("$FORM{'email'} is an invalid email address",0); } ## End unless

@requiredfields = split(/,/, $requiredjoinfields);
foreach $field (@requiredfields) {
  if ($FORM{$field} eq "") {
    &ErrorHandle::errormessage("The field $field is required",0);
  } ## End if
} ## End loop


my %swaplist = ("::name::" => "$FORM{'name'}",
"::company::" => "$FORM{'company'}",
"::payee::" => "$FORM{'payee'}",
"::address1::" => "$FORM{'address1'}",
"::address2::" => "$FORM{'address2'}",
"::city::" => "$FORM{'city'}",
"::area::" => "$FORM{'area'}",
"::postcode::" => "$FORM{'postcode'}",
"::country::" => "$FORM{'country'}",
"::website::" => "$FORM{'website'}",
"::email::" => "$FORM{'email'}",
"::ssn::" => "$FORM{'ssn'}",
"::username::" => "$FORM{'username'}",
"::password::" => "$FORM{'password'}",
"::type::" => "$FORM{'type'}",
"::paypal::" => "$FORM{'paypal'}",
"::extrafield1::" => "$FORM{'extrafield1'}",
"::extrafield2::" => "$FORM{'extrafield2'}",
"::extrafield3::" => "$FORM{'extrafield3'}",
"::extrafield4::" => "$FORM{'extrafield4'}");
if ($FORM{'type'} eq "comm") { $swaplist{'::typer::'} = "Commission"; } ## End if
if ($FORM{'type'} eq "flat") { $swaplist{'::typer::'} = "Flat Per Sale"; } ## End if


if ($WHATWANT{'want'} eq "stage1") {
  &CommonSub::TemplateParseAndDisplay("$systempath$slash$joinuppage",%swaplist);
} ## End if
else {
  my $filename = "adminpass.txt";
  open(INF,"$systempath$slash$filename");
    $userpass = <INF>;
  close(INF);
  chomp($userpass);
  ($username, $pwd) = split(/:/, $userpass);
  
  $new_password = crypt($FORM{'password'},substr($pwd, 0, 2));
  
$filedata = qq~$FORM{'username'}
name = $FORM{'name'}
company = $FORM{'company'}
payee = $FORM{'payee'}
address1 = $FORM{'address1'}
address2 = $FORM{'address2'}
city = $FORM{'city'}
area = $FORM{'area'}
postcode = $FORM{'postcode'}
country = $FORM{'country'}
website = $FORM{'website'}
email = $FORM{'email'}
ssn = $FORM{'ssn'}
username = $FORM{'username'}
password = $new_password
type = $FORM{'type'}
paypal = $FORM{'paypal'}
extrafield1 = $FORM{'extrafield1'}
extrafield2 = $FORM{'extrafield2'}
extrafield3 = $FORM{'extrafield3'}
extrafield4 = $FORM{'extrafield4'}~;
  
  my $filename = "$FORM{'username'}";
  &CommonSub::WriteToFile("$systempath$slash$data_path$slash$filename",$filedata);
  
  my $filename = "userlist.txt";
  &CommonSub::AppendToFile("$systempath$slash$data_path$slash$filename","$FORM{'username'}\n");
  
  my $filename = "$FORM{'username'}.pdy";
  &CommonSub::AppendToFile("$systempath$slash$data_path$slash$filename","0¦$months[$mon]$year\n");
  
  ##################################################
  ######################## E-mail Webmaster & Host
  ##################################################
  
  my $emailtexthost = $mailhostjoin . $filedata;
  my $emailtextuser = $mailuserjoin . $filedata;
  
  if ($operatingsystem) {
    &CommonSub::SendEmail("$mailprog",$FORM{'name'},$FORM{'email'},$companyname,$recipient,$mailuserjoinsubject,$emailtextuser,0);
    &CommonSub::SendEmail("$mailprog",$companyname,$recipient,$FORM{'name'},$FORM{'email'},$mailhostjoinsubject,$emailtexthost,0);
  } ## End if
  else {
    &CommonSub::SendEmailNT("$mailprog",$FORM{'name'},$FORM{'email'},$companyname,$recipient,$mailuserjoinsubject,$emailtextuser,0,$recipient);
    &CommonSub::SendEmailNT("$mailprog",$companyname,$recipient,$FORM{'name'},$FORM{'email'},$mailhostjoinsubject,$emailtexthost,0,$recipient);
  } ## End else

  &CommonSub::TemplateParseAndDisplay("$systempath$slash$joinuppage2",%swaplist);
} ## End else


