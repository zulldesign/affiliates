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

$validdomains = "yourdomain.com¦yourcreditcardprocessordomain.com";
$thankyoupage = "thankyou.html";
$blockinvaliddomains = 0;

##################################################
######################## OS independant code
##################################################

$|=1;

## Choose operating system

BEGIN {
  if (($^O eq 'MSWin32') || defined($ENV{'OS'})) {
    ##### Get ENV
    unless ($ENV{'PATH_TRANSLATED'} || $ENV{'SCRIPT_FILENAME'}) {
      $aspmode = 1;
      $ENV{'PATH_TRANSLATED'} = $Request->ServerVariables('PATH_TRANSLATED')->item;
      $ENV{'SCRIPT_FILENAME'} = $Request->ServerVariables('SCRIPT_FILENAME')->item;
    } ## End unless
    $operatingsystem = 0;
    $operatingsystemoldnt = 0;
    $systempath = "$ENV{'PATH_TRANSLATED'}";
    unless ($systempath) {
      $systempath = "$ENV{'SCRIPT_FILENAME'}";
    } ## End unless
    unless ($systempath) {
      $systempath = "$ENV{'SCRIPT_NAME'}";
    } ## End unless
    $systempath =~ s/\\/\//gis;
    ($systempath, $extention) = $systempath =~ /^(.*)\/.*\.(.*)$/;
#    $operatingsystemoldnt = 1;
#    $slash = '\\';
    $slash = '/';
  } ## End if
  else {
    $operatingsystem = 1;
    $systempath = "$ENV{'SCRIPT_FILENAME'}";
    unless ($systempath) {
      $systempath = "$ENV{'SCRIPT_NAME'}";
    } ## End unless
    if ($systempath =~ /cgiwrap/) {
      $systempath = "$ENV{'PATH_TRANSLATED'}";
    } ## End if
    ($systempath, $extention) = $systempath =~ /^(.*)\/.*\.(.*)$/;
    $slash = '/';
  } ## End else
## $systempath = "systempath to your folder"; ## Enter the correct value and un-comment this if you are having system path detection problems
  push (@INC, "$systempath");
} ## End BEGIN

use CGI::Carp 'fatalsToBrowser';
use cosmic;
if ($aspmode) {
  require ASP;
  $e = Win32::OLE::Enum->new($Request->ServerVariables);
  for($e->All())	{
    $ENV{$_} = $Request->ServerVariables($_)->item;
  } ## End loop
} ## End if

unless ($aspmode) {print "Content-type: text/html\n\n";} ## End unless

if ($blockinvaliddomains) {
  $domainvalid = 0;
  @validdomains = split(/¦/,$validdomains);
  foreach $domain (@validdomains) {
    chomp($domain);
    if ($ENV{'HTTP_REFERER'} =~ m|https?://([^/]*)$domain|i) {
      $domainvalid = 1;
    } ## End if
  } ## End loop
  unless ($domainvalid) {
    exit;
  } ## End unless
} ## End if


##################################################
######################## Show User posted data
##################################################

my %WHATWANT = &CommonSub::get_get_data;
my %FORM = &CommonSub::get_post_data;

open(INF,"$systempath$slash$thankyoupage");
  my @userdata = <INF>;
close(INF);

unless (exists $WHATWANT{'id'}) {
  $WHATWANT{'id'} = $ENV{'REMOTE_ADDR'}; ## Use IP for ID if none passed
} ## End unless
if (exists $WHATWANT{'cbreceipt'}) {
  $WHATWANT{'id'} = $WHATWANT{'cbreceipt'}; ## ClickBank ID
} ## End if
if (exists $FORM{'txn_id'}) {
  $WHATWANT{'id'} = $FORM{'txn_id'}; ## PayPal ID
  unless (exists $WHATWANT{'amount'}) {
    $WHATWANT{'amount'} = $FORM{'mc_gross'};
  } ## End if
} ## End if
if (exists $FORM{'order-id'}) {
  $WHATWANT{'id'} = $FORM{'order-id'}; ## PlugnPay ID
  unless (exists $WHATWANT{'amount'}) {
    $WHATWANT{'amount'} = $FORM{'card-amount'};
  } ## End if  
} ## End if
if (exists $FORM{'x_amount'}) {
  $WHATWANT{'id'} = $FORM{'x_invoice_num'}; ## PlugnPay ID
  unless (exists $WHATWANT{'amount'}) {
    $WHATWANT{'amount'} = $FORM{'x_amount'};
  } ## End if  
} ## End if
if (exists $FORM{'x_trans_id'}) {
  $WHATWANT{'id'} = $FORM{'x_trans_id'}; ## 2CheckOut ID
  unless (exists $WHATWANT{'amount'}) {
    $WHATWANT{'amount'} = $FORM{'x_amount'};
  } ## End if  
} ## End if


$CONTENT = join('',@userdata);
$CONTENT =~ s/::id::/$WHATWANT{'id'}/gis;
$CONTENT =~ s/::amount::/$WHATWANT{'amount'}/gis;

print "$CONTENT";













