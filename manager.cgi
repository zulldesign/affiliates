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
chomp($w3cdate);
chomp($time);

%WHATWANT = &CommonSub::get_get_data;

our $backandmainhtml = "<br><font size=\"2\"><a href=\"javascript:history.back(1)\">back</a> | <a href=\"manager.cgi?want=enteradmin&session=$WHATWANT{'session'}\">main</a></font>";
our $backhtml = "<br><font size=\"2\"><a href=\"javascript:history.back(1)\">back</a></font>";


if ($WHATWANT{'want'} eq "admin") {
  &admin();
} ## End if
elsif ($WHATWANT{'want'} eq "logout") {
  &logout();
} ## End if
elsif ($WHATWANT{'want'} eq "enteradmin") {
  %FORM = &CommonSub::get_post_data();
  my $filename = "adminpass.txt";
  open(INF,"$systempath$slash$filename"); ## Open read file
    $adminpass = <INF>; ## Put into an array
  close(INF); ## Close file
  ($adminname, $apass) = split(/:/, $adminpass);
  $test_passwd = crypt($FORM{'password'}, substr($apass, 0, 2)); ## see if input password matches one on file
  if ($test_passwd ne $apass || $adminname ne $FORM{'username'}) {
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
    &ErrorHandle::errormessage("Your session has expired. Please re-login.$backhtml",0);
  } ## End unless
} ## End else

if ($WHATWANT{'want'} eq "this") {
  &this();
} ## End if
if ($WHATWANT{'want'} eq "last") {
  &last();
} ## End if
if ($WHATWANT{'want'} eq "monthlycomm") {
  &monthlycomm();
} ## End if
if ($WHATWANT{'want'} eq "due") {
  &paydue();
} ## End if
if ($WHATWANT{'want'} eq "paydayconfirm") {
  &paydayconfirm();
} ## End if
if ($WHATWANT{'want'} eq "payday") {
  &payday();
} ## End if
if ($WHATWANT{'want'} eq "emailform") {
  &emailform();
} ## End if
if ($WHATWANT{'want'} eq "sendmail") {
  &sendmail();
} ## End if
if ($WHATWANT{'want'} eq "newadmin") {
  &newadmin();
} ## End if
if ($WHATWANT{'want'} eq "displayaffiliates") {
  &displayaffiliates();
} ## End if
if ($WHATWANT{'want'} eq "removeaffiliate") {
  &removeaffiliate();
} ## End if
if ($WHATWANT{'want'} eq "displayorders") {
  &displayorders();
} ## End if
if ($WHATWANT{'want'} eq "removeorder") {
  &removeorder();
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
######################## Month stats
##################################################

sub monthstats {

my $workingmonth = $_[0];

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management<br>
      <font size="2">Commission for $workingmonth</font></font></p>
      <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">back</a></font></p>
<body>
    <table width="400" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td><table border="0" cellpadding="6" cellspacing="1" width="400">
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Per 
                  Affiliate </font></div></td>
            </tr>
            <tr> 
              <td width="100%" bgcolor="#FFFFFF"><table width="100%" border="0" cellspacing="0" cellpadding="2">
EndHTML
;

$totalsalesb = 0;
my $filename = "userlist.txt";
open(INF,"$systempath$slash$data_path$slash$filename"); ## Open read file
  @userdata = <INF>; ## Put into an array
close(INF); ## Close file
foreach $line (@userdata) { ## Start main loop
  chomp($line);
  $clickdata = $line.$workingmonth;
  %USERINFO = &GetUserInfo($line);
  $amounttotal = 0;

  open(INF,"$systempath$slash$data_path$slash$clickdata"); ## Open read file
    @userdata2 = <INF>; ## Put into an array
  close(INF); ## Close file
  $totalsales = @userdata2;
  $totalsalesb += $totalsales;
  foreach $line2 (@userdata2) { ## Start of loop
    chomp($line2);
    ($id, $amount, $datea) = split(/¦/,$line2);
    $amounttotal += $amount;
    $amounttotalb += $amount;
  } ## End loop

  if ($USERINFO{'type'} eq "comm") { $affiliatetotal = ($commission/100) * $amounttotal; } ## End if
  else { $affiliatetotal = $totalsales * $flatrate; } ## End else
  
  $affiliatetotal = &CommonSub::FormatNum2DPLong($affiliatetotal);
  $affiliatetotal = &CommonSub::FormatNum2DP($affiliatetotal);

  $totalrev += $affiliatetotal;
  
  print <<EndHTML;
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$line</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$affiliatetotal</font></td>
                  </tr>
EndHTML
;
} ## End loop

$amounttotalb = &CommonSub::FormatNum2DPLong($amounttotalb);
$amounttotalb = &CommonSub::FormatNum2DP($amounttotalb);
$totalrev = &CommonSub::FormatNum2DPLong($totalrev);
$totalrev = &CommonSub::FormatNum2DP($totalrev);

print <<EndHTML;
                </table></td>
            </tr>
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Totals</font></div></td>
            </tr>
            <tr> 
              <td bgcolor="#FFFFFF"><table width="100%" border="0" cellspacing="0" cellpadding="2">
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Total 
                      sales Value:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$amounttotalb</font></td>
                  </tr>
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Total 
                      sales:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$totalsalesb</font></td>
                  </tr>
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      commission percentage:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$commission\%</font></td>
                  </tr>
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      flat rate payment:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$flatrate</font></td>
                  </tr>
                  <tr>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      commission:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$totalrev</font></td>
                  </tr>
                </table>
                
              </td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>

EndHTML
;

} ## End sub


##################################################
######################## This month earnings
##################################################

sub this {

&monthstats("$months[$mon]$year");

} ## End sub


##################################################
######################## Last month earnings
##################################################

sub last {

my $lastmonth = $mon - 1;
my $passyear = $year;
if ($lastmonth < 0) {
  $lastmonth = 11;
  $passyear--;
} ## End if

&monthstats("$months[$lastmonth]$passyear");

} ## End sub


##################################################
######################## Monthly Comm
##################################################

sub monthlycomm {

&monthstats("$WHATWANT{'month'}$WHATWANT{'year'}");

} ## End sub


##################################################
######################## Enter admin
##################################################

sub admin {

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<div align="center"> 
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>
<p><font face="Verdana, Arial, Helvetica, sans-serif" size="4">Password required 
    for Management Area</font></p>
  <form action="manager.cgi?want=enteradmin" method="POST">
    <table width="250" border="0" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr>
        <td><table width="250" border="0" cellpadding="4" cellspacing="1">
            <tr bgcolor="#FFFFFF"> 
              <td><font face="Verdana, Arial, Helvetica, sans-serif">Username</font></td>
              <td> 
                <input type="text" size="20"
    name="username"> </td>
            </tr>
            <tr bgcolor="#FFFFFF"> 
              <td><font face="Verdana, Arial, Helvetica, sans-serif">Password</font></td>
              <td> 
                <input type="password" size="20"
    name="password"> </td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center"> 
      <input type="hidden" value="enteradmin" name="want">
      <input type="submit" value="Enter">
    </p>
    </form>
  <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program powered 
    by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
    <a href="http://www.allaffiliatepro.com">affiliate software</a> from the makers 
    of AllAffiliatePro<br>
    <a href="http://www.cosmicscripts.com">free 
    cgi scripts</a> from CosmicScripts.com<br>
    <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</div>
</body>
</html>
EndHTML
;

} ## End sub


##################################################
######################## Main page
##################################################

sub mainpage {

my $monthselect = qq~<select name="month">\n~;
foreach $monther (@months) {
  $monthselect .= qq~<option value="$monther">$monther</option>\n~;
} ## End loop
$monthselect .= qq~</select>\n~;

my $yearselect = qq~<select name="year">\n~;
my $tmpyear = $yearstart;
my $yearto = $year + 1;
until ($tmpyear eq $yearto) {
  $yearselect .= qq~<option value="$tmpyear">$tmpyear</option>\n~;
  $tmpyear++;
} ## End loop
$yearselect .= qq~</select>\n~;

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td>
<p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management</font></p>
    <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=logout&session=$WHATWANT{'session'}">logout</a></font></p>
    <table width="400" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td><table border="0" cellpadding="6" cellspacing="1" width="400">
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Statistics</font></div></td>
            </tr>
            <tr> 
              <td width="100%" bgcolor="#FFFFFF"><p><font size="3" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=this&session=$WHATWANT{'session'}">Affiliate 
                earnings this month</a><br>
                <a href="manager.cgi?want=last&session=$WHATWANT{'session'}">Affiliate 
                earnings last month</a><br>
                <a href="manager.cgi?want=due&session=$WHATWANT{'session'}&period=this">Affiliate 
                earnings this PayPeriod</a><br>
                <a href="manager.cgi?want=due&session=$WHATWANT{'session'}&period=last">Affiliate 
                earnings last PayPeriod</a></font></p>
                <form action=manager.cgi  method="get">
                  <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Monthly 
                    Commissions:-</font></p>
                  <table width="250" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
                    <tr> 
                      <td><table width="250" border="0" cellpadding="4" cellspacing="1">
                          <tr bgcolor="#FFFFFF"> 
                            <td bgcolor="#FFFFFF"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Month</font></td>
                            <td>$monthselect</td>
                          </tr>
                          <tr bgcolor="#FFFFFF"> 
                            <td bgcolor="#FFFFFF"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Year</font></td>
                            <td>$yearselect</td>
                          </tr>
                        </table></td>
                    </tr>
                  </table>
                  <input name="session" type="hidden" id="session" value="$WHATWANT{'session'}">
                  <input name="want" type="hidden" id="want" value="monthlycomm">
                  <center>
                    <input name="submit" type=submit value="Show Stats">
                  </center>
                </form>
              </td>
            </tr>
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Functions</font></div></td>
            </tr>
            <tr> 
              <td bgcolor="#FFFFFF"><p><a href="manager.cgi?want=paydayconfirm&session=$WHATWANT{'session'}"><font face="Verdana, Arial, Helvetica, sans-serif">Generate 
                  PayDay</font></a><font face="Verdana, Arial, Helvetica, sans-serif"><br>
                  <a href="manager.cgi?want=displayaffiliates&session=$WHATWANT{'session'}">Display 
                  Affiliates</a><br>
                  <a href="manager.cgi?want=displayorders&session=$WHATWANT{'session'}&period=this">Display 
		  Order History this period</a><br>
		  <a href="manager.cgi?want=displayorders&session=$WHATWANT{'session'}&period=last">Display 
                  Order History last period</a><br>
                  <a href="manager.cgi?want=emailform&session=$WHATWANT{'session'}">Email 
                  all Affiliates</a></font></p>
                 <form action=manager.cgi?want=newadmin&session=$WHATWANT{'session'}  method="POST">
                  <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Enter new 
    admin password:-</font></p>
  <table width="250" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
    <tr> 
      <td><table width="250" border="0" cellpadding="4" cellspacing="1">
          <tr bgcolor="#FFFFFF"> 
            <td bgcolor="#FFFFFF"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Username</font></td>
            <td> <input type="text" size="20"
    name="username"> </td>
          </tr>
          <tr bgcolor="#FFFFFF"> 
            <td bgcolor="#FFFFFF"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Password</font></td>
            <td> <input type="password" size="20"
    name="password"> </td>
          </tr>
          <tr bgcolor="#FFFFFF"> 
            <td bgcolor="#FFFFFF"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Repeat Password</font></td>
            <td> <input type="password" size="20"
    name="password2"> </td>
          </tr>
        </table></td>
    </tr>
  </table>
  <center><input type=submit value="Save New Password"></center>
</form></p></td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>


EndHTML
;

} ## End sub


##################################################
######################## Payday Confirm
##################################################

sub paydayconfirm {

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management<br>
      <font size="2">PayDay Generation</font></font></p>
<body>
    <table width="400" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td><table border="0" cellpadding="6" cellspacing="1" width="400">
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font color="#CC0000" size="4" face="Verdana, Arial, Helvetica, sans-serif"><strong>!!This 
                  cannot be undone!!</strong></font></div></td>
            </tr>
            <tr> 
              <td width="100%" bgcolor="#FFFFFF"><table width="100%" border="0" cellspacing="0" cellpadding="6">
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Go 
                      Back </font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">Back</a></font></td>
                  </tr>
                  <tr> 
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Continue</font></td>
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=payday&session=$WHATWANT{'session'}">Generate 
                      PayDay</a></font></td>
                  </tr>
                </table></td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>

EndHTML
;

} ## End sub


##################################################
######################## Generate payday
##################################################

sub payday {

my $usersales = 0;
my $userpay = 0;
my $filename = "userlist.txt"; 
open(INF,"$systempath$slash$data_path$slash$filename");
  @userdata = <INF>;
close(INF);
foreach $line (@userdata) {
  chomp($line);
  $usersales = 0;
  $userpay = 0;
  ($lastpaydayamount,$workingmonthyear,$amountb,$lastdateb) = &lastpayout($line);
  
  %USERINFO = &GetUserInfo($line);
  
  until ($workingmonthyear eq "$months[$mon]$year") {
  
    $clickdata = "$line$workingmonthyear";
    open(INF,"$systempath$slash$data_path$slash$clickdata");
      @userdata2 = <INF>;
    close(INF);
    $usersales += @userdata2;
    foreach $line2 (@userdata2) {
      chomp($line2);
      ($id, $amount, $datea) = split(/¦/,$line2);
      $userpay += $amount;
    } ## End loop

    $workingmonthyear = &nextmonthyear($workingmonthyear);
  
  } ## End until

  if ($USERINFO{'type'} eq "comm") { $commissionamount = ($commission/100)*$userpay; }
  else { $commissionamount = $flatrate*$usersales; }
  $commissionamount = &CommonSub::FormatNum2DPLong($commissionamount);
  $commissionamount = &CommonSub::FormatNum2DP($commissionamount);
  $USERPAYLIST{$line} = $commissionamount;

} ## End main loop


foreach $key (keys(%USERPAYLIST)) {
  if ($USERPAYLIST{$key} >= $minimumpay) {
    ($lastpaydayamount,$lastpaydaymonthyear,$amountb,$lastdateb) = &lastpayout($key);
    if ($wipeold && ($lastdateb ne "NILL")) {
      $workingmonthyear = $lastdateb;
      until ($workingmonthyear eq $lastpaydaymonthyear) {
        $clickdata = "$key$workingmonthyear";
        unlink("$systempath$slash$data_path$slash$clickdata");
        $workingmonthyear = &nextmonthyear($workingmonthyear);
      } ## End until
    } ## End if
    
    ### Add to .pdy files
    my $filename = "$key.pdy";
    &CommonSub::AppendToFile("$systempath$slash$data_path$slash$filename","$USERPAYLIST{$key}¦$months[$mon]$year\n");

    ### Open user file for email
    %USERINFO = &GetUserInfo($key);

    ### CSV gateway
    $EXCELFILE{$key} = "$USERINFO{'name'}¦$USERINFO{'address1'}¦$USERINFO{'address2'}¦$USERINFO{'city'}¦$USERINFO{'area'}¦$USERINFO{'postcode'}¦$USERINFO{'country'}¦$USERINFO{'ssn'}¦$USERINFO{'website'}¦$USERINFO{'email'}¦$USERINFO{'username'}¦$USERINFO{'type'}¦$USERINFO{'paypal'}¦$USERINFO{'extrafield1'}¦$USERINFO{'extrafield2'}¦$USERINFO{'extrafield3'}¦$USERINFO{'extrafield4'}¦$USERPAYLIST{$key}";

    $paydaydata = qq~
Total Commissions: $USERPAYLIST{$key}

Affiliate Details:-
name = $USERINFO{'name'}
address1 = $USERINFO{'address1'}
address2 = $USERINFO{'address2'}
city = $USERINFO{'city'}
area = $USERINFO{'area'}
postcode = $USERINFO{'postcode'}
country = $USERINFO{'country'}
website = $USERINFO{'website'}
email = $USERINFO{'email'}
ssn = $USERINFO{'ssn'}
username = $USERINFO{'username'}
password = $new_password
type = $USERINFO{'type'}
paypal = $USERINFO{'paypal'}
extrafield1 = $USERINFO{'extrafield1'}
extrafield2 = $USERINFO{'extrafield2'}
extrafield3 = $USERINFO{'extrafield3'}
extrafield4 = $USERINFO{'extrafield4'}~;

    ### E-mail Webmaster & Host
    if ($operatingsystem) {
      &CommonSub::SendEmail("$mailprog",$companyname,$recipient,$USERINFO{'name'},$USERINFO{'email'},$mailhostpaydaysubject,"$mailhostpayday$paydaydata",0);
      &CommonSub::SendEmail("$mailprog",$USERINFO{'name'},$USERINFO{'email'},$companyname,$recipient,$mailuserpaydaysubject,"$mailuserpayday$paydaydata",0);
    } ## End if
    else {
      &CommonSub::SendEmailNT("$mailprog",$companyname,$recipient,$USERINFO{'name'},$USERINFO{'email'},$mailhostpaydaysubject,"$mailhostpayday$paydaydata",0,$recipient);
      &CommonSub::SendEmailNT("$mailprog",$USERINFO{'name'},$USERINFO{'email'},$companyname,$recipient,$mailuserpaydaysubject,"$mailuserpayday$paydaydata",0,$recipient);
    } ## End else
  } ## End if
} ## End loop


### CSV gateway
my $affiliatepayhtml;
my $outfiledata = qq~Payout for $months[$mon]$year,,,,,,,,,,\n
Name,Address1,Address2,Town/City,Area/Province,Postcode/Zip,Country,SSN,Website,E-mail,Username,Type,PayPal,Extrafield1,Extrafield2,Extrafield3,Extrafield4,Payment Due\n~;
foreach $key (keys(%EXCELFILE)) {
  ($nameb, $address1b, $address2b, $cityb, $area, $postcodeb, $countryb, $ssnb, $websiteb, $emailb, $usernameb,$typeb,$paypalb,$extrafield1b,$extrafield2b,$extrafield3b,$extrafield4b,$payoutb) = split(/¦/, $EXCELFILE{$key});
  $outfiledata .= qq~$nameb,$address1b,$address2b,$cityb,$area,$postcodeb,$countryb,$ssnb,$websiteb,$emailb,$usernameb,$typeb,$paypalb,$extrafield1b,$extrafield2b,$extrafield3b,$extrafield4b,$payoutb\n~;
  $affiliatepayhtml .= "<br>$usernameb - $payoutb\n";
} ## End loop
my $filename = "payday$months[$mon]$year.csv";
&CommonSub::AppendToFile("$systempath$slash$payday_path$slash$filename",$outfiledata);

&ErrorHandle::message("Operation Complete","The PayDay has been generated. All emails have been sent and $filename spreadsheet file generated. The following affiliates have been paid:-<br>$affiliatepayhtml$backandmainhtml",0);

} ## End sub main


##################################################
######################## Pay due
##################################################

sub paydue {

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management<br>
      <font size="2">Commission Due $WHATWANT{'period'} PayPeriod</font></font></p>
      <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">back</a></font></p>
<body>
    <table width="400" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td><table border="0" cellpadding="6" cellspacing="1" width="400">
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Per 
                  Affiliate </font></div></td>
            </tr>
            <tr> 
              <td width="100%" bgcolor="#FFFFFF"><table width="100%" border="0" cellspacing="0" cellpadding="2">
EndHTML
;

my $totalpayduea = 0;
my $totalpayduemina = 0;
my $amounttotalb = 0;
my $totalsalesb = 0;
my $usersales = 0;
my $userpay = 0;
my $filename = "userlist.txt"; 
open(INF,"$systempath$slash$data_path$slash$filename");
  @userdata = <INF>;
close(INF);
foreach $line (@userdata) {
  chomp($line);
  $usersales = 0;
  $userpay = 0;
  ($lastpaydayamount,$workingmonthyear,$amountb,$lastdateb) = &lastpayout($line);
  
  %USERINFO = &GetUserInfo($line);
  
  my $monthyearto = &nextmonthyear("$months[$mon]$year");
  my $monthyearfrom = $workingmonthyear;
  if ($WHATWANT{'period'} eq "last") {
    if ($lastdateb eq "NILL") {
      $monthyearto = $workingmonthyear;
      $monthyearfrom = $workingmonthyear;
    } ## End if
    else {
      $monthyearto = $workingmonthyear;
      $monthyearfrom = $lastdateb;
    } ## End else
  } ## End elsif
  
  until ($monthyearfrom eq $monthyearto) {
  
    $clickdata = "$line$monthyearfrom";
    open(INF,"$systempath$slash$data_path$slash$clickdata");
      @userdata2 = <INF>;
    close(INF);
    $usersales += @userdata2;
    $totalsalesb += $usersales;
    foreach $line2 (@userdata2) {
      chomp($line2);
      ($id, $amount, $datea) = split(/¦/,$line2);
      $amounttotalb += $amount;
      $userpay += $amount;
    } ## End loop

    $monthyearfrom = &nextmonthyear($monthyearfrom);
  
  } ## End until

  if ($USERINFO{'type'} eq "comm") { $commissionamount = ($commission/100)*$userpay; }
  else { $commissionamount = $flatrate*$usersales; }
  $USERPAYLIST{$line} = $commissionamount;
  
  $commissionamount = &CommonSub::FormatNum2DPLong($commissionamount);
  $commissionamount = &CommonSub::FormatNum2DP($commissionamount);

  print <<EndHTML;
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$line</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$commissionamount</font></td>
                  </tr>
EndHTML
;

  $totalpayduea += $commissionamount;
  if ($commissionamount >= $minimumpay) {
    $totalpayduemina += $commissionamount;
  } ## End if
} ## End main loop

$amounttotalb = &CommonSub::FormatNum2DPLong($amounttotalb);
$amounttotalb = &CommonSub::FormatNum2DP($amounttotalb);
$totalpayduea = &CommonSub::FormatNum2DPLong($totalpayduea);
$totalpayduea = &CommonSub::FormatNum2DP($totalpayduea);
$totalpayduemina = &CommonSub::FormatNum2DPLong($totalpayduemina);
$totalpayduemina = &CommonSub::FormatNum2DP($totalpayduemina);

print <<EndHTML;

                </table></td>
            </tr>
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Totals</font></div></td>
            </tr>
            <tr> 
              <td bgcolor="#FFFFFF"><table width="100%" border="0" cellspacing="0" cellpadding="2">
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Total 
                      sales Value:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$amounttotalb</font></td>
                  </tr>
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Total 
                      sales:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$totalsalesb</font></td>
                  </tr>
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      commission percentage:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$commission\%</font></td>
                  </tr>
                  <tr> 
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      flat rate payment:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$flatrate</font></td>
                  </tr>
                  <tr>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      commissions:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$totalpayduea</font></td>
                  </tr>
                  <tr>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                      commissions > min:</font></td>
                    <td><font face="Verdana, Arial, Helvetica, sans-serif">$currency$totalpayduemina</font></td>
                  </tr>
                </table>
              </td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>

EndHTML
;

} ## End sub


##################################################
######################## Display Affiliates
##################################################

sub displayaffiliates {

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management<br>
      <font size="2">Current Affiliates</font></font></p>
      <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">back</a></font></p>
<body>
    <table width="98%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td><table border="0" cellpadding="6" cellspacing="1" width="100%">
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Current 
                  Affiliates</font><font color="#CC0000" size="4" face="Verdana, Arial, Helvetica, sans-serif"><strong> 
                  </strong></font></div></td>
            </tr>
            <tr> 
              <td width="100%" bgcolor="#FFFFFF"><table width="100%" border="0" cellspacing="0" cellpadding="6">
                  <tr> 
                    <td><strong><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Affiliate 
                      Username</font></strong></td>
                    <td><strong><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Order 
                      history</font></strong></td>
                    <td><strong><font size="2" face="Verdana, Arial, Helvetica, sans-serif">View 
                      Info </font></strong></td>
                    <td><strong><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Email</font></strong></td>
                    <td><strong><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Remove</font></strong></td>
                  </tr>

EndHTML
;

my $filename = "userlist.txt";
open(INF,"$systempath$slash$data_path$slash$filename");
  @userdata = <INF>;
close(INF);
foreach $user (@userdata) {
  chomp($user);
  %USERINFO = &GetUserInfo($user);
  print <<EndHTML;
                  <tr> 
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif">$USERINFO{'username'}</font></td>
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=displayorders&session=$WHATWANT{'session'}&affiliate=$USERINFO{'username'}&period=this">This</a> 
                      <a href="manager.cgi?want=displayorders&session=$WHATWANT{'session'}&affiliate=$USERINFO{'username'}&period=last">Last</a></font></td>
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=affiliateinfo&session=$WHATWANT{'session'}&affiliate=$USERINFO{'username'}">Info</a></font></td>
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="mailto:$USERINFO{'email'}">Email affiliate</a></font></td>
                    <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=removeaffiliate&session=$WHATWANT{'session'}&affiliate=$USERINFO{'username'}">Remove</a></font></td>
                  </tr>
EndHTML
;
} ## End loop

print <<EndHTML;
                </table></td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>
EndHTML
;

} ## End sub


##################################################
######################## Remove affiliate
##################################################

sub removeaffiliate {

my $filename = "userlist.txt";
open(INF,"$systempath$slash$data_path$slash$filename");
  @userdata = <INF>;
close(INF);
open(OUTF,">$systempath$slash$data_path$slash$filename");
  foreach $line (@userdata) {
    chomp($line);
    unless ($line eq $WHATWANT{'affiliate'}) {
      print OUTF
      "$line\n";
    } ## End unless
  } ## End loop
close(OUTF); ## Close file

open(INF,"$systempath$slash$data_path$slash$WHATWANT{'affiliate'}.pdy"); ## Open read file
  $paydayline = <INF>; ## Put into an array
close(INF); ## Close file
chomp($paydayline);
my ($tmp,$paydaymonthyear) = split(/¦/, $paydayline);

$workingmonthyear = $paydaymonthyear;
until ($workingmonthyear eq "$months[$mon]$year") {
  $clickdata = "$WHATWANT{'affiliate'}$workingmonthyear";
  unlink("$systempath$slash$data_path$slash$clickdata");
  $workingmonthyear = &nextmonthyear($workingmonthyear);
  unlink("$systempath$slash$data_path$slash$WHATWANT{'affiliate'}$workingmonthyear");
} ## End until
unlink("$systempath$slash$data_path$slash$WHATWANT{'affiliate'}");
unlink("$systempath$slash$data_path$slash$WHATWANT{'affiliate'}.pdy");

&ErrorHandle::message("Operation Complete","User $WHATWANT{'affiliate'} has been removed$backandmainhtml",0);

} ## End sub


##################################################
######################## Display Orders
##################################################

sub displayorders {

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management<br>
      <font size="2">Affiliate Order History $WHATWANT{'period'} period</font></font></p>
      <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">back</a></font></p>
<body>
    <table width="400" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td> 
          <table width="100%" border="0" cellspacing="1" cellpadding="4">
            <tr bgcolor="#D2EBFF"> 
              <td><font face="Verdana, Arial, Helvetica, sans-serif">OrderID</font></td>
              <td><font face="Verdana, Arial, Helvetica, sans-serif">Amount</font></td>
              <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif">Remove</font></td>
            </tr>

EndHTML
;

$totalpayduea = 0;
$totalpayduemina = 0;
$amounttotalb = 0;
$totalsalesb = 0;
$usersales = 0;
my $filename = "userlist.txt"; 
open(INF,"$systempath$slash$data_path$slash$filename");
  @userdata = <INF>;
close(INF);
foreach $line (@userdata) {
  chomp($line);
  if ($WHATWANT{'affiliate'} && $line ne $WHATWANT{'affiliate'}) {
    next;
  } ## End if
  ($lastpaydayamount,$workingmonthyear,$amountb,$lastdateb) = &lastpayout($line);
  
  my $monthyearto = &nextmonthyear("$months[$mon]$year");
  my $monthyearfrom = $workingmonthyear;
  if ($WHATWANT{'period'} eq "last") {
    if ($lastdateb eq "NILL") {
      $monthyearto = $workingmonthyear;
      $monthyearfrom = $workingmonthyear;
    } ## End if
    else {
      $monthyearto = $workingmonthyear;
      $monthyearfrom = $lastdateb;
    } ## End else
  } ## End elsif
  
  %USERINFO = &GetUserInfo($line);

  print <<EndHTML;
            <tr bgcolor="#FFFFFF"> 
              <td colspan="3"><div align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">$line</font></div></td>
            </tr>
EndHTML
;
  
  until ($monthyearfrom eq $monthyearto) {
  
    $clickdata = "$line$monthyearfrom";
    open(INF,"$systempath$slash$data_path$slash$clickdata");
      @userdata2 = <INF>;
    close(INF);
    foreach $line2 (@userdata2) {
      chomp($line2);
      ($id, $amount, $datea) = split(/¦/,$line2);
      print <<EndHTML;
            <tr bgcolor="#FFFFFF"> 
              <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif">$id</font></td>
              <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif">$amount</font></td>
              <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="manager.cgi?want=removeorder&session=$WHATWANT{'session'}&id=$id&filename=$clickdata">Remove</a></font></td>
            </tr>
EndHTML
;

    } ## End loop
    $monthyearfrom = &nextmonthyear($monthyearfrom);
  } ## End until
} ## End main loop

print <<EndHTML;

          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>

EndHTML
;

} ## End sub


##################################################
######################## Remove Order
##################################################

sub removeorder {

open(INF,"$systempath$slash$data_path$slash$WHATWANT{'filename'}");
  @userdata = <INF>;
close(INF);
open(OUTF,">$systempath$slash$data_path$slash$WHATWANT{'filename'}");
  foreach $line (@userdata) {
    chomp($line);
    ($id, $amount, $datea) = split(/¦/,$line);
    unless ($id eq $WHATWANT{'id'}) {
      print OUTF
      "$line\n";
    } ## End unless
  } ## End loop
close(OUTF);

&ErrorHandle::message("Operation Complete","The order number $WHATWANT{'id'} has been removed$backandmainhtml",0);

} ## End sub


##################################################
######################## Email Form
##################################################

sub emailform {

print <<EndHTML;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>AffiliateClick Management Area</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#ffffff" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>  
<table width="100%" border="0" cellspacing="0" cellpadding="10">
  
<tr> 
  <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif" size="4"><br>
      AffiliateClick Management<br>
      <font size="2">Email your Affiliates</font></font></p>
<body>
    <table width="500" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#000000">
      <tr> 
        <td><table border="0" cellpadding="6" cellspacing="1" width="100%">
            <tr> 
              <td bgcolor="#D2EBFF"><div align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Email 
                  all Affiliates</font><font color="#CC0000" size="4" face="Verdana, Arial, Helvetica, sans-serif"><strong> 
                  </strong></font></div></td>
            </tr>
            <tr> 
              <td width="100%" bgcolor="#FFFFFF">
<form action="manager.cgi?want=sendmail&session=$WHATWANT{'session'}" method="POST">
                  <table width="100%" border="0" cellspacing="0" cellpadding="4">
                    <tr> 
                      <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Subject 
                        </font></td>
                      <td><input type="text" size="40" name="subject"></td>
                    </tr>
                    <tr> 
                      <td><font size="2" face="Verdana, Arial, Helvetica, sans-serif">HTML?</font></td>
                      <td><select name="html" id="html">
                          <option value="1">Yes</option>
                          <option value="0" selected>No</option>
                        </select></td>
                    </tr>
                  </table>
                  <p align="center"> 
                    <TEXTAREA name="emailtext" rows="14" cols="50"></TEXTAREA>
                  </p>
    <p align="center"><input type="submit" value="Send"></p>
</form></td>
            </tr>
          </table></td>
      </tr>
    </table>
    <p align="center">&nbsp;</p>
    <p align="center"><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate 
      Program powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
      <a href="http://www.allaffiliatepro.com">affiliate software</a> from the 
      makers of AllAffiliatePro<br>
      <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
      <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
</body>
</html>

EndHTML
;

} ## End sub


##################################################
######################## Get emails
##################################################

sub sendmail {

my $filename = "userlist.txt";
open(INF,"$systempath$slash$data_path$slash$filename");
  @userdata = <INF>;
close(INF);
foreach $line (@userdata) {
  chomp($line);
  %USERINFO = &GetUserInfo($line);
  $EMAILLIST{$USERINFO{'email'}} = $USERINFO{'name'};
} ## End loop

%FORM = &CommonSub::get_post_data();
foreach $key (keys(%EMAILLIST)) {
  if ($operatingsystem) {
    &CommonSub::SendEmail("$mailprog",$EMAILLIST{$key},$key,$companyname,$recipient,$FORM{'subject'},$FORM{'emailtext'},$FORM{'htmlemail'});
  } ## End if
  else {
    &CommonSub::SendEmailNT("$mailprog",$EMAILLIST{$key},$key,$companyname,$recipient,$FORM{'subject'},$FORM{'emailtext'},$FORM{'htmlemail'},$recipient);
  } ## End else
} ## End loop

&ErrorHandle::message("Operation Complete","Your affiliates have been emailed!$backhtml",0);

} ## End sub


##################################################
######################## New Admin
##################################################

sub newadmin {

%FORM = &CommonSub::get_post_data;

if ($FORM{'password'} ne $FORM{'password2'}) {
  &ErrorHandle::errormessage("Passwords do not match, please re-input$backhtml",0);
} ## End if

my ($filename) = "adminpass.txt";
open(INF,"$systempath$slash$filename");
  $userpass = <INF>;
close(INF);
chomp($userpass);
($username, $password) = split(/:/, $userpass);
$newpasscrypt = crypt($FORM{'password'}, substr($password, 0, 2));
open(OUTF,">$systempath$slash$filename");
  print OUTF
  "$FORM{'username'}:$newpasscrypt";
close(OUTF);

my $loginlink = "<br><font size=\"2\"><a href=\"manager.cgi?want=admin\">LOGIN</a></font>";

&ErrorHandle::message_end("Operation Complete","Your new username/password combination has been saved$loginlink",0);

} ## End sub


##################################################
######################## Affiliate Info
##################################################

sub affiliateinfo {

%USERINFO = &GetUserInfo($WHATWANT{'affiliate'});

if ($USERINFO{'type'} eq "comm") { $typer = "Commission"; } ## End if
if ($USERINFO{'type'} eq "flat") { $typer = "Flat Per Sale"; } ## End if

print <<EndHTML;

<html>
<head>
<title>Affiliate Info</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#FFFFFF" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="20">
  <tr>
    <td> <p align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Affiliate 
        information<br>
        <font size="2">Update affiliate information</font></font>
      <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">back</a></font>
      <form action="manager.cgi?want=infoupdate&session=$WHATWANT{'session'}&affiliate=$WHATWANT{'affiliate'}" method="POST">
        <center>
          <table border="0" cellspacing="0" cellpadding="0">
            <tr> 
              <td bgcolor="#000000"> <table border=0 cellspacing=1 cellpadding=4 bordercolor="#000000" >
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Name</font></td>
                    <td bgcolor="#CCCCFF"><input name="name" type="text" value="$USERINFO{'name'}" size="20"></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Company</font></td>
                    <td bgcolor="#D2EBFF"><input name="company" type="text" value="$USERINFO{'company'}" size="20"></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Checks 
                      payable to</font></td>
                    <td bgcolor="#CCCCFF"><input name="payee" type="text" value="$USERINFO{'payee'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Address 
                      1</font></td>
                    <td bgcolor="#D2EBFF"><input name="address1" type="text" value="$USERINFO{'address1'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Address 
                      2</font></td>
                    <td bgcolor="#CCCCFF"><input name="address2" type="text" id="address2" value="$USERINFO{'address2'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Town/City</font></td>
                    <td bgcolor="#D2EBFF"><input name="city" type="text" id="city" value="$USERINFO{'city'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Area/Province</font></td>
                    <td bgcolor="#CCCCFF"><input name="area" type="text" value="$USERINFO{'area'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Post 
                      Code/Zip</font></td>
                    <td bgcolor="#D2EBFF"><input name="postcode" type="text" value="$USERINFO{'postcode'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Country</font></td>
                    <td bgcolor="#CCCCFF"><input name="country" type="text" value="$USERINFO{'country'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Website 
                      URL</font></td>
                    <td bgcolor="#D2EBFF"><input name="website" type="text" value="$USERINFO{'website'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">E-mail</font></td>
                    <td bgcolor="#CCCCFF"><input name="email" type="text" value="$USERINFO{'email'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">SS# 
                      or Tax I.D.</font> <font face="Verdana, Arial, Helvetica, sans-serif" size="3"><br>
                      required for US applicants</font></td>
                    <td bgcolor="#D2EBFF"><input name="ssn" type="text" value="$USERINFO{'ssn'}" size="20"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">PayPal 
                      E-mail</font></td>
                    <td bgcolor="#CCCCFF"><input name="paypal" type="text" value="$USERINFO{'paypal'}" size="20"> 
                    </td>
                  </tr>
                  <!--extrafield1start-->
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra 
                      Field 1</font></td>
                    <td bgcolor="#D2EBFF"> <input name="extrafield1" type="text" value="$USERINFO{'extrafield1'}" size="20"> 
                    </td>
                  </tr>
                  <!--extrafield1end-->
                  <!--extrafield2start-->
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra 
                      Field 2</font></td>
                    <td bgcolor="#CCCCFF"> <input name="extrafield2" type="text" value="$USERINFO{'extrafield2'}" size="20"> 
                    </td>
                  </tr>
                  <!--extrafield2end-->
                  <!--extrafield3start-->
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra 
                      Field 3</font></td>
                    <td bgcolor="#D2EBFF"> <input name="extrafield3" type="text" value="$USERINFO{'extrafield3'}" size="20"> 
                    </td>
                  </tr>
                  <!--extrafield3end-->
                  <!--extrafield4start-->
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra 
                      Field 4</font></td>
                    <td bgcolor="#CCCCFF"> <input name="extrafield4" type="text" value="$USERINFO{'extrafield4'}" size="20"> 
                    </td>
                  </tr>
                  <!--extrafield4end-->
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">UserName</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif">$USERINFO{'username'}
                      </font> </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">New 
                      Password</font></td>
                    <td bgcolor="#CCCCFF"> <input name="password" type="text" size="20" maxlength="8"> 
                    </td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Type</font></td>
                    <td bgcolor="#D2EBFF"> <font face="Verdana, Arial, Helvetica, sans-serif">$typer
                      </font></td>
                  </tr>
                  <tr>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif">Change 
                      Type</font></td>
                    <td bgcolor="#CCCCFF"><select name="newtype" size="1">
                        <option selected value="">---No Change---</option>
                        <option value="comm">Commission</option>
                        <option value="flat">Flat per sale</option>
                      </select></td>
                  </tr>
                </table></td>
            </tr>
          </table>
        </center>

<center>
          <input name="username" type="hidden" id="username" value="$USERINFO{'username'}">
          <input name="type" type="hidden" id="type" value="$USERINFO{'type'}">
          <input type="submit" value="Send Application"></center>
</form>
      <div align="center">
        <p>&nbsp;</p>
        <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program 
          powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
          <a href="http://www.allaffiliatepro.com">affiliate software</a> from 
          the makers of AllAffiliatePro<br>
          <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
          <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
        </div></td>
  </tr>
</table>
</body>
</html>

EndHTML
;

} ## End sub

##################################################
######################## Info Update
##################################################

sub infoupdate {

%FORM = &CommonSub::get_post_data();

%USERINFO = &GetUserInfo($FORM{'username'});

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

if ($FORM{'type'} eq "comm") { $typer = "Commission"; } ## End if
if ($FORM{'type'} eq "flat") { $typer = "Flat Per Sale"; } ## End if

print <<EndHTML;

<!doctype html public "-//w3c//dtd html 4.0 transitional//en">
<html>
<head>
<title>Affiliate Info</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#FFFFFF" topmargin=0 marginheight=0 leftmargin=0 marginwidth=0 rightmargin=0>
<table width="100%" border="0" bgcolor="#000000">
  <tr>
    <td height="66"> 
      <div align="center"><font size="5" color="#66CCFF"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="6">COS<font color="#FFCC66">M</font>IC</font></b><font face="Verdana, Arial, Helvetica, sans-serif" size="6" color="#FFFFFF">PERL</font><font size="6" color="#FFFFFF"><font color="#6699CC" face="Verdana, Arial, Helvetica, sans-serif">&#153;</font></font></font></div>
    </td>
  </tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="20">
  <tr>
    <td><p align="center"><font face="Verdana, Arial, Helvetica, sans-serif">Affiliate 
        Info <br>
        <font size="2">Updated information:-</font></font> 
      <p align="center"><font size="2" face="Verdana, Arial, Helvetica, sans-serif"><a href="javascript:history.back(1)">back</a></font>
      <center>
          <table border="0" cellspacing="0" cellpadding="0">
            <tr> 
              <td bgcolor="#000000"> <table width="100%" border=0 cellpadding=4 cellspacing=1 bordercolor="#000000" >
                <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Name</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'name'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Company</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'company'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Checks payable to</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'payee'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Address 1</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'address1'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Address 2</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'address2'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Town/City</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'city'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Area/Province</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'area'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Post Code/Zip</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'postcode'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Country</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'country'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Website URL</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'website'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">E-mail</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'email'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">SS# 
                      or Tax I.D.</font> <font face="Verdana, Arial, Helvetica, sans-serif" size="3"><br>
                      required for US applicants</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'ssn'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">PayPal E-mail</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'paypal'}</font></td>
                  </tr>
                  <!--extrafield1start-->
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra Field 1</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'extrafield1'}</font></td>
                  </tr>
                  <!--extrafield1end-->
                  <!--extrafield2start-->
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra Field 2</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'extrafield2'}</font></td>
                  </tr>
                  <!--extrafield2end-->
                  <!--extrafield3start-->
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra Field 3</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'extrafield3'}</font></td>
                  </tr>
                  <!--extrafield3end-->
                  <!--extrafield4start-->
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Extra Field 4</font></td>
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'extrafield4'}</font></td>
                  </tr>
                  <!--extrafield4end-->
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">UserName</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">$FORM{'username'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Password</font></td>
                    
                  <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif">$FORM{'password'}</font></td>
                  </tr>
                  <tr> 
                    <td bgcolor="#CCCCFF"><font face="Verdana, Arial, Helvetica, sans-serif" size="3">Type</font></td>
                    <td bgcolor="#D2EBFF"><font face="Verdana, Arial, Helvetica, sans-serif">$typer</font></td>
                  </tr>
                </table></td>
            </tr>
          </table>
        </center>
      <div align="center">
        <p><font size="2" face="verdana,arial,helvetica,tahoma"></font></p>
        <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program 
          powered by <a href="http://www.cosmicperl.com">CosmicPerl.com</a><br>
          <a href="http://www.allaffiliatepro.com">affiliate software</a> from 
          the makers of AllAffiliatePro<br>
          <a href="http://www.cosmicscripts.com">free cgi scripts</a> from CosmicScripts.com<br>
          <a href="http://www.cosmicperl.com">cgi scripts</a> from CosmicPerl.com</font></p>
      </div></td>
  </tr>
</table>
</body>
</html>

EndHTML
;

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
######################## Log Out
##################################################

sub logout {

my $stimeout = $sessiontimeout * 60;
our %SESSION = &CommonSub::GetSession($WHATWANT{'session'},"$systempath$slash$data_path","logout$stimeout");
&ErrorHandle::message("Log Out Successful","You have been logged out<br><a href=\"manager.cgi?want=admin\">Log back in</a>",0);

} ## End sub




