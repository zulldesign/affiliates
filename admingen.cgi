#!/usr/bin/perl
##-----------------------------------------------------------------##
##                                                                 ##
##                                                                 ##
## © Copyright Mr Lyle R Hopkins 2001. All rights reserved. No part##
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
######################## Other variables
##################################################

print "Content-type: text/html\n\n";

$|=1;

## Choose operating system

BEGIN {
  if (($^O eq 'MSWin32') || defined($ENV{'OS'})) {
    $operatingsystem = 0;
    $operatingsystemoldnt = 0;
    $systempath = "$ENV{'PATH_TRANSLATED'}";
    $systempath =~ s/(\\[a-z0-9]*\.cgi)$//g;
    unless ($systempath) {
      $systempath = "$ENV{'SCRIPT_FILENAME'}";
      $systempath =~ s/(\/[a-z0-9]*\.cgi)$//g;
    } ## End unless
#    $operatingsystemoldnt = 1;
#    $slash = '\\';
    $slash = '/';
  } ## End if
  else {
    $operatingsystem = 1;
    $systempath = "$ENV{'SCRIPT_FILENAME'}";
    $systempath =~ s/(\/[a-z0-9]*\.cgi)$//g;
    if ($systempath =~ /cgiwrap/) {
      $systempath = "$ENV{'PATH_TRANSLATED'}";
      $systempath =~ s/(\/[a-z0-9]*\.cgi)$//g;
    } ## End if
    $slash = '/';
  } ## End else
## $systempath = "systempath to your folder"; ## Enter the correct value and un-comment this if you are having system path detection problems
  push (@INC, "$systempath");
} ## End BEGIN


use cosmic;
%WHATWANT = &CommonSub::get_get_data();

unless ($WHATWANT{'want'} eq "start2") {
  &chmodcheck;
} ## End if

sub chmodcheck {
  my $filename = "adminpass.txt";
  chmod(0777, "$systempath$slash$filename") || &chmoderror;
} ## End sub


sub chmoderror {
  my $filename = "adminpass.txt";
  unless (-w "$systempath$slash$filename") {
    &ErrorHandle::errormessage("You must chmod adminpass.txt 777 or enable write permissions",0);
  } ## End unless
} ## End sub


##################################################
######################## Start
##################################################

$adminstyle1 = "*.pU8Tz9HKBtM";
$adminstyle2 = "*.pbnMU1TaBfU";
$passcrypt = crypt("adminpass", substr($adminstyle1, 0, 2));
if ($passcrypt ne $adminstyle1){
  $passcrypt = crypt("adminpass", substr($adminstyle2, 0, 2));
  if ($passcrypt ne $adminstyle2){
    &ErrorHandle::errormessage("There is a problem with your server encryption capabilities please contact our support, visit <a href=\"http://www.cosmicperl.com\">CosmicPerl.com</a>",0);
  } ## End if
} ## End if

my $filename = "adminpass.txt";
chmod(0777, "$systempath$slash$filename");

open(OUTF,">$systempath$slash$filename");
  print OUTF "admin:$passcrypt";
close(OUTF);

&ErrorHandle::message("Operation Complete","Your adminpass.txt file has been generated.<br>Username: admin<br>Password: adminpass<br> You must now delete this cgi file (admingen.cgi) to prevent hackers from damaging your system.",0);
