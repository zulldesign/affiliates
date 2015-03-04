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
######################## Other variables
##################################################

print "Content-type:text/html\n\n";

$mainpage = "menu.html";
$statspage = "statspage.html";
$updatepage = "updatepage.html";
$updatedonepage = "updatedonepage.html";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$month = ($mon + 1);
$month = sprintf("%02d", $month);
$mday = sprintf("%02d", $mday);
$year += 1900;
$date = "$year$month$mday";
$time = sprintf("%02d:%02d:%02d", $hour,$min,$sec);
@months = ("January","February","March","April","May","June","July","August","September","October","November","December");
%monthshash = ("January" => 0,"February" => 1,"March" => 2,"April" => 3,"May" => 4,"June" => 5,"July" => 6,"August" => 7,"September" => 8,"October" => 9,"November" => 10,"December" => 11);
@days = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
## Clean date and time
$thstrder = "th";
if ($mday == 1) { $thstrder = "st"; } ## End if
if ($mday == 2) { $thstrder = "nd"; } ## End if
if ($mday == 3) { $thstrder = "rd"; } ## End if
$datewords = "$days[$wday] $mday$thstrder $months[$mon]";
chomp($date);
chomp($time);

%WHATWANT = &CommonSub::get_get_data;

our $backhtml = "<br><font size=\"2\"><a href=\"javascript:history.back(1)\">back</a></font>";


if ($WHATWANT{'want'} eq "admin") {
  &admin();
} ## End if
elsif ($WHATWANT{'want'} eq "logout") {
  &logout();
} ## End if
elsif ($WHATWANT{'want'} eq "enteradmin") {
  %FORM = &CommonSub::get_post_data();
  unless (-e "$systempath$slash$data_path$slash$FORM{'username'}") {
    &ErrorHandle::errormessage("Invalid Username$backhtml",0);
  } ## End if
  %USERINFO = &GetUserInfo($FORM{'username'});
  $test_passwd = crypt($FORM{'password'}, substr($USERINFO{'password'}, 0, 2));
  if ($test_passwd ne $USERINFO{'password'}) {
    &ErrorHandle::errormessage("Incorrect password$backhtml",0);
  } ## End if
  &makesession($FORM{'username'},$FORM{'password'});
  $WHATWANT{'session'} = $SESSION{'id'};
  &mainpage();
} ## End if
else {
  my $stimeout = $sessiontimeout * 60;
  our %SESSION = &CommonSub::GetSession($WHATWANT{'session'},"$systempath$slash$data_path",$stimeout);
  unless ($SESSION{name}) {
    &ErrorHandle::errormessage("Your session has expired. Please re-login.<br><a href=\"$statsloginurl\">Login</a>",0);
  } ## End unless
} ## End else

if ($WHATWANT{'want'} eq "monthly") {
  &monthly();
} ## End if
if ($WHATWANT{'want'} eq "paydue") {
  &paydue();
} ## End if
if ($WHATWANT{'want'} eq "lastpay") {
  &lastpay();
} ## End if
if ($WHATWANT{'want'} eq "affiliateinfo") {
  &affiliateinfo();
} ## End if
if ($WHATWANT{'want'} eq "infoupdate") {
  &infoupdate();
} ## End if


##################################################
######################## Make Session
##################################################

sub makesession {
my ($sessionuser, $sessionpass) = @_;

my @chars=('A'..'Z','a'..'z',0..9);
my $id = join('',@chars[map{rand @chars}(1..32)]);

my $stimeout = $sessiontimeout * 60;

### Create session
our %SESSION = &CommonSub::GetSession($id,"$systempath$slash$data_path",$stimeout,$sessionuser,$sessionpass);
#print " $SESSION{'pass'} $SESSION{'name'}";

} ## End sub


##################################################
######################## Main page
##################################################

sub mainpage {

my ($paydue, $totalsales, $totalpay) = &AffiliateEarn($SESSION{'name'},"this");
%swaplist = ("::session::" => $WHATWANT{'session'},
"::paydue::" => $paydue,
"::programurl::" => $programurl,
"::username::" => $SESSION{'name'},
"::currency::" => $currency);
&CommonSub::TemplateParseAndDisplay("$systempath$slash$mainpage",%swaplist);

} ## End sub


##################################################
######################## Monthly earnings
##################################################

sub monthly {

if ($WHATWANT{'month'} eq "current") {
  $WHATWANT{'month'} = $months[$mon];
} ## End if
elsif ($WHATWANT{'month'} eq "lastmon") {
  $lastmon = $mon - 1;
  if ($lastmon < 0) {
    $lastmon = 11;
  } ## End if
  $WHATWANT{'month'} = $months[$lastmon];
} ## End elsif

my ($paydue, $totalsales, $totalvalue) = &AffiliateEarn($SESSION{'name'},$WHATWANT{'month'});

%swaplist = ("::session::" => $WHATWANT{'session'},
"::paydue::" => $paydue,
"::stats::" => "$WHATWANT{'month'}",
"::programurl::" => $programurl,
"::totalsales::" => $totalsales,
"::salevalue::" => $totalvalue,
"::commissionp::" => $commission,
"::flatrate::" => $flatrate,
"::username::" => $SESSION{'name'},
"::currency::" => $currency);
&CommonSub::TemplateParseAndDisplay("$systempath$slash$statspage",%swaplist);

} ## End sub


##################################################
######################## Pay due
##################################################

sub paydue {

my ($paydue, $totalsales, $totalvalue) = &AffiliateEarn($SESSION{'name'},"this");
%swaplist = ("::session::" => $WHATWANT{'session'},
"::paydue::" => $paydue,
"::stats::" => "Current PayPeriod",
"::programurl::" => $programurl,
"::totalsales::" => $totalsales,
"::salevalue::" => $totalvalue,
"::commissionp::" => $commission,
"::flatrate::" => $flatrate,
"::username::" => $SESSION{'name'},
"::currency::" => $currency);
&CommonSub::TemplateParseAndDisplay("$systempath$slash$statspage",%swaplist);

} ## End sub


##################################################
######################## Last payout
##################################################

sub lastpay {

my ($paydue, $totalsales, $totalvalue) = &AffiliateEarn($SESSION{'name'},"last");
%swaplist = ("::session::" => $WHATWANT{'session'},
"::paydue::" => $paydue,
"::stats::" => "Last PayPeriod",
"::programurl::" => $programurl,
"::totalsales::" => $totalsales,
"::salevalue::" => $totalvalue,
"::commissionp::" => $commission,
"::flatrate::" => $flatrate,
"::username::" => $SESSION{'name'},
"::currency::" => $currency);
&CommonSub::TemplateParseAndDisplay("$systempath$slash$statspage",%swaplist);

} ## End sub


##################################################
######################## Enter admin
##################################################

sub admin {

print <<EndHTML;

<p align="center"><font size="6">Enter password to enter Admin
area</font></p>

<p align="center">&nbsp;</p>

<form action="statoa.cgi?want=enteradmin" method="POST">
    <p align="center">Username <input type="text" size="20"
    name="username"></p>
    <p align="center">Password <input type="text" size="20"
    name="password"></p>
    <p align="center"><input type="submit" value="Enter"></p>
</form>

EndHTML
;

} ## End sub


##################################################
######################## Affiliate Earn
##################################################

sub AffiliateEarn {
($affiliatename,$monther) = @_;

($lastpaydayamount,$workingmonthyear,$amountb,$lastdateb) = &lastpayout($affiliatename);

my $monthyearto = &nextmonthyear("$monther$year");
my $monthyearfrom = "$monther$year";

if ($monther eq "this") {
  $monthyearto = &nextmonthyear("$months[$mon]$year");
  $monthyearfrom = $workingmonthyear;
} ## End if
elsif ($monther eq "last") {
  if ($lastdateb eq "NILL") {
    $monthyearto = $workingmonthyear;
    $monthyearfrom = $workingmonthyear;
  } ## End if
  else {
    $monthyearto = $workingmonthyear;
    $monthyearfrom = $lastdateb;
  } ## End else
} ## End elsif

$usersales = 0;
$userpay = 0;

%USERINFO = &GetUserInfo($affiliatename);

until ($monthyearfrom eq "$monthyearto") {
  $clickdata = "$affiliatename$monthyearfrom";
  open(INF,"$systempath$slash$data_path$slash$clickdata");
    @userdata2 = <INF>;
  close(INF);
  $usersales += @userdata2;
  foreach $line2 (@userdata2) {
    chomp($line2);
    ($id, $amount, $datea) = split(/¦/,$line2);
    $userpay += $amount;
  } ## End loop
  $monthyearfrom = &nextmonthyear($monthyearfrom);
} ## End until
if ($USERINFO{'type'} eq "comm") { $commissionamount = ($commission/100)*$userpay; }
else { $commissionamount = $flatrate*$usersales; }

$commissionamount = &CommonSub::FormatNum2DPLong($commissionamount);
$commissionamount = &CommonSub::FormatNum2DP($commissionamount);
$userpay = &CommonSub::FormatNum2DPLong($userpay);
$userpay = &CommonSub::FormatNum2DP($userpay);

my @return = ($commissionamount,$usersales,$userpay);

return @return;

} ## End sub


##################################################
######################## Affiliate Info
##################################################

sub affiliateinfo {

%USERINFO = &GetUserInfo($SESSION{'name'});

my %swaplist = ("::name::" => "$USERINFO{'name'}",
"::company::" => "$USERINFO{'company'}",
"::payee::" => "$USERINFO{'payee'}",
"::address1::" => "$USERINFO{'address1'}",
"::address2::" => "$USERINFO{'address2'}",
"::city::" => "$USERINFO{'city'}",
"::area::" => "$USERINFO{'area'}",
"::postcode::" => "$USERINFO{'postcode'}",
"::country::" => "$USERINFO{'country'}",
"::website::" => "$USERINFO{'website'}",
"::email::" => "$USERINFO{'email'}",
"::ssn::" => "$USERINFO{'ssn'}",
"::username::" => "$USERINFO{'username'}",
"::password::" => "$USERINFO{'password'}",
"::type::" => "$USERINFO{'type'}",
"::paypal::" => "$USERINFO{'paypal'}",
"::extrafield1::" => "$USERINFO{'extrafield1'}",
"::extrafield2::" => "$USERINFO{'extrafield2'}",
"::extrafield3::" => "$USERINFO{'extrafield3'}",
"::extrafield4::" => "$USERINFO{'extrafield4'}",
"::session::" => "$WHATWANT{'session'}");
if ($USERINFO{'type'} eq "comm") { $swaplist{'::typer::'} = "Commission"; } ## End if
if ($USERINFO{'type'} eq "flat") { $swaplist{'::typer::'} = "Flat Per Sale"; } ## End if

&CommonSub::TemplateParseAndDisplay("$systempath$slash$updatepage",%swaplist);

} ## End sub

##################################################
######################## Info Update
##################################################

sub infoupdate {

%FORM = &CommonSub::get_post_data();

%USERINFO = &GetUserInfo($SESSION{'name'});

if ($FORM{'password'}) {
  $USERINFO{'password'} = crypt($FORM{'password'}, substr($USERINFO{'password'}, 0, 2));
} ## End if
else {
  $FORM{'password'} = "none";
} ## End else

if ($FORM{'newtype'}) {
  $FORM{'type'} = $FORM{'newtype'};
} ## End if

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
password = $USERINFO{'password'}
type = $FORM{'type'}
paypal = $FORM{'paypal'}
extrafield1 = $FORM{'extrafield1'}
extrafield2 = $FORM{'extrafield2'}
extrafield3 = $FORM{'extrafield3'}
extrafield4 = $FORM{'extrafield4'}~;

my $filename = "$FORM{'username'}";
&CommonSub::WriteToFile("$systempath$slash$data_path$slash$filename",$filedata);


##################################################
######################## E-mail Webmaster & Host
##################################################

  my $emailtexthost = $mailhostupdate . $filedata;
  my $emailtextuser = $mailuserupdate . $filedata;
  
  if ($operatingsystem) {
    &CommonSub::SendEmail("$mailprog",$FORM{'name'},$FORM{'email'},$companyname,$recipient,$mailuserupdatesubject,$emailtextuser,0);
    &CommonSub::SendEmail("$mailprog",$companyname,$recipient,$FORM{'name'},$FORM{'email'},$mailhostupdatesubject,$emailtexthost,0);
  } ## End if
  else {
    &CommonSub::SendEmailNT("$mailprog",$FORM{'name'},$FORM{'email'},$companyname,$recipient,$mailuserupdatesubject,$emailtextuser,0,$recipient);
    &CommonSub::SendEmailNT("$mailprog",$companyname,$recipient,$FORM{'name'},$FORM{'email'},$mailhostupdatesubject,$emailtexthost,0,$recipient);
  } ## End else

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

&CommonSub::TemplateParseAndDisplay("$systempath$slash$updatedonepage",%swaplist);

} ## End sub


##################################################
######################## GetUserInfo
##################################################

sub GetUserInfo {

open(INF,"$systempath$slash$data_path$slash$_[0]");
  @userinf = <INF>;
close(INF);
foreach $bitinf (@userinf) {
  chomp($bitinf);
  ($name, $value) = split(/ = /,$bitinf);
  $USERINFO{$name} = $value;
} ## End loop

return %USERINFO;

} ## End sub


##################################################
######################## Last Payout
##################################################

sub lastpayout {

open(INF,"$systempath$slash$data_path$slash$_[0].pdy");
  my @lastpaydata = <INF>;
close(INF);
my $line, $lastdate = "NILL", $amount = "NILL";
foreach $line (@lastpaydata) {
  chomp($line);
  $lastdateb = $lastdate;
  $amountb = $amount;
  ($amount, $lastdate) = split(/¦/,$line);
} ## End loop
my @returnvar = ("$amount","$lastdate","$amountb","$lastdateb");
return @returnvar;

} ## End sub


##################################################
######################## Next Month Year
##################################################

sub nextmonthyear {

my $workingmonthyear = $_[0];
$workingmonthyear =~ /[0-9]/gis;
my $yearnumber = "$&$'";
my $monthnumber = $monthshash{$`};
$monthnumber++;
if ($monthnumber eq 12) {
  $monthnumber = 0;
  $yearnumber++;
} ## End if
$workingmonthyear = "$months[$monthnumber]$yearnumber";
return $workingmonthyear;

} ## End sub


##################################################
######################## Log Out
##################################################

sub logout {

my $stimeout = $sessiontimeout * 60;
our %SESSION = &CommonSub::GetSession($WHATWANT{'session'},"$systempath$slash$data_path","logout$stimeout");
&ErrorHandle::message("Log Out Successful","You have been logged out<br><a href=\"$statsloginurl\">Login</a><br><a href=\"$site1\">To the site</a>",0);

} ## End sub


