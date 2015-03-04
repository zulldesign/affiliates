package ErrorHandle;
### Routines to display messages and errors
sub errormessage {
### Displays an error message and exits with optional html header
  if ($_[1]) { print "Content-type:text/html\n\n"; } ## End if
  print <<EndHTML
    <center>
  <table width="400" border="1" cellspacing="0" cellpadding="10" bordercolor="#000000">
    <tr>
      <td bgcolor="#000000">
        <div align="center">
          <p><font face="verdana" size=5 color="#FF0000">An error has occurred</font></p>
          <p><font face="verdana" size="3" color="#FFFFFF">$_[0]</font></p>
        </div>
      </td>
    </tr>
  </table>
  <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program powered 
    by <a href="http://www.cosmicperl.com">CosmicPerl.com</a></font><br>
    <font face="Verdana, Arial, Helvetica, sans-serif" size="1">Check our site 
    for the latest updates, and new products.</font> </p>
</center>
EndHTML
;
  exit;
}
sub errornote {
### Displays an error message with optional html header
  if ($_[1]) { print "Content-type:text/html\n\n"; } ## End if
  print <<EndHTML
<center>
  <table width="400" border="1" cellspacing="0" cellpadding="10" bordercolor="#000000">
    <tr>
      <td bgcolor="#000000">
        <div align="center">
          <p><font face="verdana" size=5 color="#FF0000">An error MAY have occurred</font></p>
          <p><font face="verdana" size="3" color="#FFFFFF">$_[0]</font></p>
        </div>
      </td>
    </tr>
  </table>

  <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program powered 
    by <a href="http://www.cosmicperl.com">CosmicPerl.com</a></font><br>
    <font face="Verdana, Arial, Helvetica, sans-serif" size="1">Check our site 
    for the latest updates, and new products.</font> </p>
</center>
EndHTML
;
}
sub message {
### Displays a message and title text with optional html header
  if ($_[2]) { print "Content-type:text/html\n\n"; } ## End if
  print <<EndHTML
    <center>
  <table width="400" border="1" cellspacing="0" cellpadding="10" bordercolor="#000000">
    <tr> 
      <td bgcolor="#FFFF99"> 
        <div align="center"> 
          <p><font face="verdana" size=5 color="#0000FF">$_[0]</font></p>
        </div>
      </td>
    </tr>
    <tr>
      <td><font face="verdana" size="3" color="#000000">$_[1]</font></td>
    </tr>
  </table>

  <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program powered 
    by <a href="http://www.cosmicperl.com">CosmicPerl.com</a></font><br>
    <font face="Verdana, Arial, Helvetica, sans-serif" size="1">Check our site 
    for the latest updates, and new products.</font> </p>
</center>
EndHTML
;
}
sub message_end {
### Displays a message and title text then exits with optional html header
  if ($_[2]) { print "Content-type:text/html\n\n"; } ## End if
  print <<EndHTML
    <center>
  <table width="400" border="1" cellspacing="0" cellpadding="10" bordercolor="#000000">
    <tr> 
      <td bgcolor="#FFFF99"> 
        <div align="center"> 
          <p><font face="verdana" size=5 color="#0000FF">$_[0]</font></p>
        </div>
      </td>
    </tr>
    <tr>
      <td><font face="verdana" size="3" color="#000000">$_[1]</font></td>
    </tr>
  </table>

  <p><font size="1" face="verdana,arial,helvetica,tahoma">Affiliate Program powered 
    by <a href="http://www.cosmicperl.com">CosmicPerl.com</a></font><br>
    <font face="Verdana, Arial, Helvetica, sans-serif" size="1">Check our site 
    for the latest updates, and new products.</font> </p>
</center>
EndHTML
;
  exit;
}

package CommonSub;
### A variety of common routines
sub get_post_data {
### Get's POST form data
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
  @pairs = split(/&/, $buffer);
  foreach $pair (@pairs) {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $name =~ tr/+/ /;
    $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    if (exists $FORM{$name}) {
      $FORM{$name} .= "¦$value";
    } ## End if
    else {
      $FORM{$name} = $value;
    } ## End else
  }
  return %FORM;
} ## End sub
sub get_get_data {
### Get's GET form data
  @values = split(/\&/,$ENV{'QUERY_STRING'});
  foreach $i (@values) {
    ($varname, $mydata) = split(/=/,$i);
    $mydata =~ tr/+/ /;
    $mydata =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $varname =~ tr/+/ /;
    $varname =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $WHATWANT{$varname} = $mydata;
  }
  return %WHATWANT;
} ## End sub


##################################################
######################## Remove a single line number from a file
##################################################

sub RemoveLineNumberFromFile {
### Removes a set line number from a file
my ($FILENAME, $REMOVELINE) = @_;

my ($LINEREMOVED) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $linenum = 1;
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    if ($linenum == $REMOVELINE) {
      $LINEREMOVED = $line;
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
    $linenum++;
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return $LINEREMOVED;

} ## End sub


##################################################
######################## Remove line's from a file
##################################################

sub RemoveLineNumbersFromFile {
### Removes multiple lines from a file
my ($FILENAME, @REMOVELINES) = @_;

my (@LINESREMOVED);

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $linenum = 1;
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    if ($REMOVELINES[$linenum]) {
      push(@LINESREMOVED, $line);
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
    $linenum++;
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return @LINESREMOVED;

} ## End sub


##################################################
######################## Remove line's from a file Hash
##################################################

sub RemoveLineNumbersFromFileHash {
### Remove multiple lines from a file using a hash
my ($FILENAME, %REMOVELINES) = @_;

my (@LINESREMOVED);

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $linenum = 1;
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    if ($REMOVELINES{$linenum}) {
      push(@LINESREMOVED, $line);
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
    $linenum++;
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return @LINESREMOVED;

} ## End sub


##################################################
######################## Remove a single line from a file
##################################################

sub RemoveLineFromFile {
### Removes a line with a set piece of data from a file
my ($FILENAME, $REMOVEDATA, $DELIMITER, $DATAPOSITION) = @_;

my ($LINEREMOVED) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    my @linedata = split(/$DELIMITER/, $line);
    if ($linedata[$DATAPOSITION] eq $REMOVEDATA) {
      $LINEREMOVED = $line;
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return $LINEREMOVED;

} ## End sub


##################################################
######################## Remove line's from a file
##################################################

sub RemoveLinesFromFile {
### Removes lines with a set piece of data from a file
my ($FILENAME, %REMOVEDATA, $DELIMITER, $DATAPOSITION) = @_;

my (@LINESREMOVED);

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    my @linedata = split(/$DELIMITER/, $line);
    if ($REMOVEDATA{$linedata[$DATAPOSITION]}) {
      push(@LINESREMOVED, $line);
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return @LINESREMOVED;

} ## End sub


##################################################
######################## Modify a single line number from a file
##################################################

sub ModifyLineNumberFromFile {
### Replaces a line number with a new line
my ($FILENAME, $LINENUMBER, $NEWLINE) = @_;

my ($LINEMODIFIED) = 0;
$LINENUMBER--;
open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
$filearray[$LINENUMBER] = "$NEWLINE\n";
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $line;
  foreach $line (@filearray) {
    print OUTF "$line";
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return $LINEMODIFIED;

} ## End sub


##################################################
######################## Modify a single line from a file
##################################################

sub ModifyLineFromFile {
### Modifies a line with set piece of data from a file
my ($FILENAME, $KEYDATA, $DELIMITER, $DATAPOSITION, $NEWLINE) = @_;

my ($LINEMODIFIED) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    my @linedata = split(/$DELIMITER/, $line);
    if ($linedata[$DATAPOSITION] eq $KEYDATA) {
      $LINEMODIFIED = $line;
      print OUTF "$NEWLINE\n";
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return $LINEMODIFIED;

} ## End sub


##################################################
######################## Modify a single line from a file Advanced
##################################################

sub ModifyLineFromFileAdv {
### Modifies a line with set piece of data from a file, creating the new line from an array
my ($FILENAME, $KEYDATA, $DELIMITER, $DATAPOSITION, @NEWLINE) = @_;

my ($LINEMODIFIED) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);
open(OUTF,">$FILENAME");
  flock(OUTF,2);
  my $line;
  foreach $line (@filearray) {
    chomp($line);
    my @linedata = split(/$DELIMITER/, $line);
    if ($linedata[$DATAPOSITION] eq $KEYDATA) {
      my $datapiece;
      for ($datapiece = 0; $datapiece <= $#NEWLINE; $datapiece++) {
        if ($NEWLINE[$datapiece] eq "SAVEOLDDATA") {
          $NEWLINE[$datapiece] = $linedata[$datapiece];
        } ## End if
      } ## End loop
      my ($NEWLINE) = join($DELIMITER,@NEWLINE);
      $LINEMODIFIED = $line;
      print OUTF "$NEWLINE\n";
    } ## End if
    else {
      print OUTF "$line\n";
    } ## End else
  } ## End loop
  flock(OUTF,8);
close(OUTF);

return $LINEMODIFIED;

} ## End sub


##################################################
######################## If Data Exists In File
##################################################

sub IfDataExistsInFile {
### Checks if a piece of data exists in a file
my ($FILENAME, $KEYDATA, $DELIMITER, $DATAPOSITION) = @_;

my ($DATAEXISTS) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);

my $line;
foreach $line (@filearray) {
  chomp($line);
  my @linedata = split(/$DELIMITER/, $line);
  if ($linedata[$DATAPOSITION] eq $KEYDATA) {
    $DATAEXISTS = 1;
  } ## End if
} ## End loop

return $DATAEXISTS;

} ## End sub


##################################################
######################## How Many Data In File
##################################################

sub HowManyDataInFile {
### Returns how many pieces of set data are in a file
my ($FILENAME, $DATAPOSITION, $DELIMITER, $KEYDATA) = @_;

my ($HOWMANYDATA) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);

my $line;
foreach $line (@filearray) {
  chomp($line);
  my @linedata = split(/$DELIMITER/, $line);
  if ($linedata[$DATAPOSITION] eq $KEYDATA) {
    $HOWMANYDATA++;
  } ## End if
} ## End loop

return $HOWMANYDATA;

} ## End sub


##################################################
######################## LinesInFile
##################################################

sub LinesInFile {
### Returns the number of lines in a file
my ($FILENAME) = @_;

my ($LINESINFILE) = 0;

open(INF,"$FILENAME");
  my @filearray = <INF>;
close(INF);

$LINESINFILE = @filearray;

return $LINESINFILE;

} ## End sub


##################################################
######################## Append to file
##################################################

sub AppendToFile {
### Appends data to the end of a file
my ($FILENAME, $FILELINE) = @_;
my ($RETURNVAR) = 1;

open(OUTF,">>$FILENAME") || &SetVariable(\$RETURNVAR,0);
  flock(OUTF,2);
  seek(OUTF,0,2);
  print OUTF "$FILELINE";
  flock(OUTF,8);
close(OUTF);

return $RETURNVAR;

} ## End sub


##################################################
######################## Set Variable
##################################################

sub SetVariable {

my ($VARIABLE, $VALUE) = @_;

$VARIABLE = $VALUE;

} ## End sub


##################################################
######################## Write to file
##################################################

sub WriteToFile {
### Rewrites a file
my ($FILENAME, $FILEDATA) = @_;
my ($RETURNVAR) = 1;

open(OUTF,">$FILENAME") || &SetVariable(\$RETURNVAR,0);
  flock(OUTF,2);
  print OUTF "$FILEDATA";
  flock(OUTF,8);
close(OUTF);

return $RETURNVAR;

} ## End sub


##################################################
######################## CopyFile
##################################################

sub CopyFile {
### Copies a file
my ($sourcefile,$newfile,$permissions) = @_;
my $VALID = 1;

## Read file
open(INF,"$sourcefile") || &SetVariable(\$VALID,0);
  my @filearray = <INF>;
close(INF);
my $content = join('',@filearray);
open(OUTF,">$newfile") || &SetVariable(\$VALID,0);
  flock(OUTF,2);
  print OUTF "$content";
  flock(OUTF,8);
close(OUTF);
chmod($permissions, "$newfile");

return ($VALID);

} ## End sub


##################################################
######################## Read file as string
##################################################

sub ReadFileAsString {
### Copies a file
my ($sourcefile) = @_;
my $VALID = 1;

## Read file
open(INF,"$sourcefile");
  my @filearray = <INF>;
close(INF);
my $content = join('',@filearray);

return ($content);

} ## End sub


##################################################
######################## Check admin password
##################################################

sub PassCheck {
### Checks an encrypted username:password file
my ($FILENAME, $USERNAME, $PASSWORD) = @_;

open(INF,"$FILENAME");
  my $adminpass = <INF>;
close(INF);
my ($adminname, $apass) = split(/:/, $adminpass);

my $test_passwd = crypt($PASSWORD, substr($apass, 0, 2));

if ($test_passwd ne $apass || $adminname ne $USERNAME) {
  &ErrorHandle::errormessage("Invalid Username/Password",0);
} ## End if

} ## End sub


##################################################
######################## Check user password
##################################################

sub UserCheck {
### Checks and encrypted user name = value file
my ($FILENAME, $USERNAME, $PASSWORD) = @_;

if (-e $FILENAME) {
  %USERINFO = GetUserData("$FILENAME");
  $test_passwd = crypt($PASSWORD, substr($USERINFO{'password'}, 0, 2));
  if ($test_passwd ne $USERINFO{'password'}) {
    &ErrorHandle::errormessage("Invalid Username/Password",0);
  } ## End if
} ## End if
else {
  &ErrorHandle::errormessage("Invalid Username/Password",0);
} ## End else

} ## End sub


##################################################
######################## Send E-Mail
##################################################

sub SendEmail {
### Unix email sending routines
my ($MAILPROGRAM, $TONAME, $TOEMAIL, $FROMNAME, $FROMEMAIL, $MAILSUBJECT, $MAILMESSAGE, $MAILHTML) = @_;

open (MAIL, "|$MAILPROGRAM -t") || print "Error opening port!!!";
  print MAIL "To: $TOEMAIL ($TONAME)\n";
  print MAIL "From: $FROMEMAIL ($FROMNAME)\n";
  print MAIL "Subject: $MAILSUBJECT\n";
  if ($MAILHTML) {
    print MAIL "Content-type:text/html\n\n";
  } ## End if
  else {
    print MAIL "\n";
  } ## End else
  print MAIL "$MAILMESSAGE";
close(MAIL);

} ## End sub


##################################################
######################## Send E-Mail NT
##################################################

sub SendEmailNT {
### Windows emailing routines using sendmail.pm and an SMTP server
my ($MAILPROGRAM, $TONAME, $TOEMAIL, $FROMNAME, $FROMEMAIL, $MAILSUBJECT, $MAILMESSAGE, $MAILHTML, $ERRORSEMAIL) = @_;

my($sender) = "\"$FROMNAME\" <$FROMEMAIL>";
my($recipienta) = "\"$TONAME\" <$TOEMAIL>";

my($sm) = new SendMail("$MAILPROGRAM");
$sm->From($sender);
$sm->To($recipienta);
$sm->ReplyTo($sender);
$sm->ErrorsTo($ERRORSEMAIL);
$sm->Subject($MAILSUBJECT);
if ($MAILHTML) {
  $sm->setMailHeader("Content-type", "text/html");
} ## End if
$sm->setMailBody($MAILMESSAGE);
if ($sm->sendMail() != 0) {
  &ErrorHandle::errormessage("Error $sm->{'error'}",0);
} ## End if

} ## End sub


##################################################
######################## Get User Data
##################################################

sub GetUserData {
### Routines for reading a name = value file
my ($FILENAME) = @_;
my (%USERINFO, @userdata);

open(INF,"$FILENAME");
  @userdata = <INF>;
close(INF);
foreach $line (@userdata) {
  chomp($line);
  ($name, $value) = split(/ = /, $line);
  $USERINFO{$name} = $value;
}
return %USERINFO;

} ## End sub


##################################################
######################## Parse In SSI
##################################################
### Parses in SSI
sub ParseInSSI {
my ($CONTENT, $SYSTEMPATHSLASH) = @_;

my $counter = 1;
while ($CONTENT =~ /\<\!-\-\#include virtual=\".*?\" \-\-\>/) {
  $& =~ /\".*?\"/;
  my $FILENAME = $&;
  $FILENAME =~ s/\"//gis;
  open(INF,"$SYSTEMPATHSLASH$FILENAME");
    my (@filedata) = <INF>;
  close(INF);
  my ($SSIHTML) = join('',@filedata);
  $FILENAME =~ s/\?/\\\?/gis;
  $CONTENT =~ s/\<\!-\-\#include virtual=\"$FILENAME\" \-\-\>/$SSIHTML/gis;
  $counter++;
  if ($counter > 100) {
    print "$CONTENT";
    exit;
  } ## End if
} ## End loop
while ($CONTENT =~ /\<\!-\-\#include file=\".*?\" \-\-\>/) {
  my $FILENAME = $&;
  open(INF,"$SYSTEMPATHSLASH$FILENAME");
    my (@filedata) = <INF>;
  close(INF);
  my ($SSIHTML) = join('',@filedata);
  $CONTENT =~ s/\<\!-\-\#include file=\"$FILENAME\" \-\-\>/$SSIHTML/gis;
  $counter++;
  if ($counter > 100) {
    print "$CONTENT";
    exit;
  } ## End if
} ## End loop

return $CONTENT;

} ## End sub


##################################################
######################## Template Parse And Display
##################################################
### Swaps a list of data into a template file then prints that file
sub TemplateParseAndDisplay {

my ($FILENAME, %SWAPLIST) = @_;

open(INF,"$FILENAME");
  my (@filedata) = <INF>;
close(INF);

my ($CONTENT) = join('',@filedata);
foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

if ($SWAPLIST{'::ssi::'}) {
  print "<b>$SYSTEMPATHSLASH</b>";
  $CONTENT = &ParseInSSI($CONTENT,$SWAPLIST{'::systempathslash::'});  
} ## End if

print "$CONTENT";

} ## End sub


##################################################
######################## Template Parse And Display 2 Parts
##################################################

sub TemplateParseAndDisplay2Parts {
### Swaps a list of data into a template file, splits into 3 parts, and returns those parts
my ($FILENAME, $BETWEENA, $BETWEENB, %SWAPLIST) = @_;

open(INF,"$FILENAME");
  my (@filedata) = <INF>;
close(INF);

my ($CONTENT) = join('',@filedata);

foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

$CONTENT =~ /$BETWEENA.*?$BETWEENB/gis;
my ($areatable) = $&;
my ($pagetop) = $`;
my ($pagebottom) = $';

return ($pagetop,$pagebottom,$areatable);

} ## End sub


##################################################
######################## Template Parse And Display 3 Parts
##################################################

sub TemplateParseAndDisplay3Parts {
### Swaps a list of data into a template file, splits into 5 parts, and returns those parts
### When the 2nd area to grab is within the first
my ($FILENAME, $BETWEENA, $BETWEENB, $BETWEENC, $BETWEEND, %SWAPLIST) = @_;

open(INF,"$FILENAME");
  my (@filedata) = <INF>;
close(INF);

my ($CONTENT) = join('',@filedata);

foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

$CONTENT =~ /$BETWEENA.*?$BETWEENB/gis;
my ($areatable) = $&;
my ($pagetop) = $`;
my ($pagebottom) = $';

$areatable =~ /$BETWEENC.*?$BETWEEND/gis;
my ($tablerow) = $&;
my ($areatop) = $`;
my ($areabottom) = $';

return ($pagetop,$pagebottom,$areatop,$areabottom,$tablerow);

} ## End sub


##################################################
######################## Template Parse And Display 3 Parts B
##################################################

sub TemplateParseAndDisplay3PartsB {
### Swaps a list of data into a template file, splits into 5 parts, and returns those parts
my ($FILENAME, $BETWEENA, $BETWEENB, $BETWEENC, $BETWEEND, %SWAPLIST) = @_;

open(INF,"$FILENAME");
  my (@filedata) = <INF>;
close(INF);

my ($CONTENT) = join('',@filedata);

foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

$CONTENT =~ /$BETWEENA.*?$BETWEENB/gis;
my ($area1) = $&;
my ($pagetop) = $`;
my ($page) = $';

$page =~ /$BETWEENC.*?$BETWEEND/gis;
my ($area2) = $&;
my ($pagemiddle) = $`;
my ($pagebottom) = $';

return ($pagetop,$pagemiddle,$pagebottom,$area1,$area2);

} ## End sub


##################################################
######################## Template Parse and Write
##################################################

sub TemplateParseAndWrite {
### Swaps a list of data into a template file then writes
my ($FILENAME, $FILESAVE, %SWAPLIST) = @_;

open(INF,"$FILENAME");
  my (@filedata) = <INF>;
close(INF);

my ($CONTENT) = join('',@filedata);
foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

open(OUTF,">$FILESAVE");
  flock(OUTF,2);
  print OUTF "$CONTENT";
  flock(OUTF,8);
close(OUTF);

} ## End sub


##################################################
######################## Template Parse
##################################################

sub TemplateParse {
### Swaps a list of data into a template file then returns the string
my ($FILENAME, %SWAPLIST) = @_;

open(INF,"$FILENAME");
  my (@filedata) = <INF>;
close(INF);

my ($CONTENT) = join('',@filedata);
foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

return $CONTENT;

} ## End sub


##################################################
######################## Parse and Write
##################################################

sub ParseAndWrite {

my ($CONTENT, $FILESAVE, %SWAPLIST) = @_;
### Swaps a list of data into a variable, writes the data, then displays
foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

open(OUTF,">$FILESAVE");
  flock(OUTF,2);
  print OUTF "$CONTENT";
  flock(OUTF,8);
close(OUTF);

print "$CONTENT";

} ## End sub


##################################################
######################## Parse and Display
##################################################

sub ParseAndDisplay {

my ($CONTENT, %SWAPLIST) = @_;
### Swaps a list of data into a variable then displays
foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop
print "$CONTENT";

} ## End sub


##################################################
######################## Parse and Return
##################################################

sub ParseAndReturn {
my ($CONTENT, %SWAPLIST) = @_;
### Swaps a list of data into a variable then displays
foreach $key (keys(%SWAPLIST)) {
  $CONTENT =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop
return $CONTENT;

} ## End sub


##################################################
######################## Upload File
##################################################

sub UploadFile {
### Uses cgi-lib.pl to upload files
my ($UPLOADDIR, $MAXFILESIZE, $FILEEXTENTIONS, $OVERWRITE) = @_;
my ($file_name);

$|=1;

eval {
  my ($required) = 'cgi-lib.pl';
  require("$required");
}; ## End eval
if ($@) { print "Cant find cgi-lib.pl"; } ## End if
my (%cgi_data, %cgi_cfn, %cgi_ct, %cgi_sfn, $ret, $buf);
$cgi_lib::writefiles = "$UPLOADDIR";
$cgi_lib::filepre = "TMP";
$cgi_lib::maxdata = $MAXFILESIZE;
$ret = &ReadParse(\%cgi_data,\%cgi_cfn,\%cgi_ct,\%cgi_sfn);
if ( !(-e $UPLOADDIR) || !(-W $UPLOADDIR) || !(-d $UPLOADDIR) ) {
  &ErrorHandle::errormessage("Invalid directory name",0);
} ## End if
if (!($cgi_cfn{'upfile'})) { 
  &ErrorHandle::errormessage("No upload file selected",0);
} ## End if
else {
  if ($cgi_cfn{'upfile'} =~ /([^\/\\]+)$/) {
    $file_name = $&;
    $file_name =~ s/^\.+//;
  } ## End if
  else {
    unlink ($cgi_sfn{'upfile'});
    &ErrorHandle::errormessage("Invalid file name",0);
  } ## End else
  my ($up_image) = $cgi_sfn{'upfile'};
  my (@fileextentions) = split(/¦/, $FILEEXTENTIONS);
  my ($extention);
  my ($extention_ok) = 0;
  foreach $extention (@fileextentions) {
    if ($file_name =~ /$extention$/gis) { 
      $up_file = $file_name;
      $extention_ok = 1;
    } ## End if
  } ## End loop
  unless ($extention_ok) {
    unlink ($cgi_sfn{'upfile'});
    $FILEEXTENTIONS =~ s/¦/, /gis;
    &ErrorHandle::errormessage("Only $FILEEXTENTIONS files allowed",0);
  } ## End unless
  if (-e "$UPLOADDIR/$file_name") {
    if ($OVERWRITE) {
      unlink ("$UPLOADDIR/$file_name");
    } ## End if
    else {
      unlink ($cgi_sfn{'upfile'});
      &ErrorHandle::errormessage("File name already exists",0);
    } ## End else
  } ## End if
  $path_image = "$UPLOADDIR/$up_file";
  link($up_image, $path_image);
  unlink ($cgi_sfn{'upfile'});
} ## End else

return $up_file;

} ## End sub


##################################################
######################## Parse And Return
##################################################

sub ParseAndReturn {
### Swaps a list of data into a string
my ($STRING, %SWAPLIST) = @_;

foreach $key (keys(%SWAPLIST)) {
  $STRING =~ s/$key/$SWAPLIST{$key}/gis;
} ## End loop

return $STRING;

} ## End sub


##################################################
######################## Check Email
##################################################

sub CheckEmail {
### Checks email address format
my ($EMAIL) = @_;
my $VALIDEMAIL = 0;

if ($EMAIL =~ /\@/) {
  if ($EMAIL =~ /\./) {
    $VALIDEMAIL = 1;
  } ## End if
} ## End if

return $VALIDEMAIL;

} ## End sub


##################################################
######################## Check Invalid Input
##################################################

sub CheckInvalidInput {
### Checks for nasty characters
my ($STRINGTOCHECK) = @_;
my ($RETURNNUM) = 0;
my $CHAR;

if ($STRINGTOCHECK =~ /\/|\\|\;|\#|\||\¬|\¦|\$|\*|\~|\{|\}|\[|\]|\<|\>|\?|\,|\=/) {
  $RETURNNUM = 1;
  $CHAR = $&;
} ## End if

@RETURN = ($RETURNNUM, $CHAR);
return @RETURN;

} ## End sub


##################################################
######################## Check Alpha only
##################################################

sub CheckAlphaOnly {
### Checks a string is lettersonly
my ($STRING) = @_;
my $VALID = 1;

if ($STRING =~ /[^a-zA-Z]/) {
  $VALID = 0;
  $INVALID = $&;
} ## End if

return ($VALID,$INVALID);

} ## End sub


##################################################
######################## Check Num only
##################################################

sub CheckNumOnly {
### Checks a sting is a number only
my ($STRING) = @_;
my $VALID = 1;

if ($STRING =~ /[^0-9\.\-]/) {
  $VALID = 0;
  $INVALID = $&;
} ## End if

return ($VALID,$INVALID);

} ## End sub


##################################################
######################## Check Alpha Num only
##################################################

sub CheckAlphaNumOnly {
### Checks a sting is numbers for letters only
my ($STRING) = @_;
my $VALID = 1;

if ($STRING =~ /[^0-9\.\-a-zA-Z]/) {
  $VALID = 0;
  $INVALID = $&;
} ## End if

return ($VALID,$INVALID);

} ## End sub


##################################################
######################## Format 2 decimal places
##################################################

sub FormatNum2DP {
### Formats a number to 2 dp (badly)
my $number = $_[0];

if ($number == 0) {
  $number = "0.00";
} ## End if
elsif ($number !~ /\./) {
  $number = "$number.00";
} ## End if
else {
  my $whole = $`;
  my $decimal = $';
  if (length($decimal) < 2) {
    $number = "$whole.$decimal" . "0";
  } ## End if
} ## End else

return $number;

} ## End sub


##################################################
######################## Format 2 decimal places for long number
##################################################

sub FormatNum2DPLong {
### Formats a long number to 2 dp
my $number = $_[0];

if ($number =~ /\./) {
  $number = $number * 100;
  $number = int($number);
  $number = $number / 100;
} ## End if

return $number;

} ## End if


##################################################
######################## Security Email Banned Characters
##################################################

sub SecurityEmailBannedChars {
### Checks email sending name and email address for hacker input
my ($email, $name) = @_;
my $return = 0;

if ($email =~ /,/ || $email =~ /;/) {
  $return = 1;
} ## End if
if ($email =~ /\:/ || $name =~ /\:/) {
  $return = 1;
} ## End if

} ## End sub


##################################################
######################## Security Email IP Logger
##################################################

sub SecurityEmailIPlogger {
### IP logger for security
my ($filename, $date) = @_;
my $iphits = 0;

open (FILE, "$filename");
  @ipblocker = <FILE>;
close (FILE);
open(OUTF,">$filename");
foreach $ipdate (@ipblocker) {
  chomp($ipdate);
  ($ip, $hitnum, $dater) = split(/¦/, $ipdate);
  if ($ip eq $ENV{'REMOTE_ADDR'}) {
    $hitnum++;
    $iphits = $hitnum;
  } ## End if
  if ($dater eq $date) {
    print OUTF "$ip¦$hitnum¦$dater\n";
  } ## End if
} ## End loop
close(OUTF); ## Close file
unless ($iphits) {
  &AppendToFile($filename,"$ENV{'REMOTE_ADDR'}¦1¦$date\n");
  $iphits = 1;
} ## End unless

return $iphits;

} ## End sub


##################################################
######################## HTML folder detection
##################################################

sub HTMLFolderDetect {
## Detects the path to the main html folder
my $systempath = $_[0];

my @htmlfolderlist = ("http","web","www","html","htdocs","httpdocs","public_html");
$htmlfolderpath = "../..";
foreach $foldername (@htmlfolderlist) {
  if (-e "$systempath" . "../../../$foldername") { $htmlfolderpath = "../../../$foldername"; } ## End if
  if (-e "$systempath" . "../../$foldername") { $htmlfolderpath = "../../$foldername"; } ## End if
  if (-e "$systempath" . "../$foldername") { $htmlfolderpath = "../$foldername"; } ## End if
} ## End loop

return $htmlfolderpath;

} ## End sub


##################################################
######################## HTML folder detection
##################################################

sub SendMailPathDetect {
### Detects the path to sendmail or qmail
my $mailprog = $_[0];

if (-e "/usr/sbin/sendmail") { $mailprog = "/usr/sbin/sendmail"; } ## End if
if (-e "/usr/bin/sendmail") { $mailprog = "/usr/bin/sendmail"; } ## End if
if (-e "/usr/lib/sendmail") { $mailprog = "/usr/lib/sendmail"; } ## End if
if (-e "/var/qmail/bin/qmail-inject") { $mailprog = "/var/qmail/bin/qmail-inject"; } ## End if

return $mailprog;

} ## End sub


##################################################
######################## Backup MySQL
##################################################

sub BackupMySQL {
### Backsup a MySQL table to a flat file
my ($DSN, $username, $password, $tablename, $fieldnames, $outputfile) = @_;
my @fieldnames = @$fieldnames;
my $records = 0;
my $success = 0;
my $outputdata = "";

foreach $field (@fieldnames) {
  $outputdata .= "$field¦";
} ## End loop
chop $outputdata;
  
&WriteToFile("$outputfile","$outputdata\n");

### Connect to DB
use DBI;
$dbh=DBI->connect($DSN,$username,$password);

### Construct select SQL using $tablename and @fieldnames
my $sql="SELECT ";
my $field;
foreach $field (@fieldnames) {
  $sql .= "$field,";
} ## End loop
chop $sql;
$sql .= " FROM $tablename";

### Call database
my $sth=$dbh->prepare($sql);
$sth->execute()  or print "Cannot get fields: $DBI::errstr<br>SQL = $sql<br>\n";
while (@fieldsarray = $sth->fetchrow_array) {
  $records++;
  my $outputdata;
  foreach $field (@fieldsarray) {
    $outputdata .= "$field¦";
  } ## End loop
  chop $outputdata;
### Write results to ¦ delimited file, clock $records
  $success = &AppendToFile("$outputfile","$outputdata\n");
} ## End loop

$dbh->disconnect();

my @return = ($success, $records);
return @return;

} ## End if


##################################################
######################## Restore MySQL
##################################################

sub RestoreMySQL {
### Restores a MySQL database table, ignoring a set field
my ($DSN, $username, $password, $tablename, $inputfile, $ignorefield) = @_;
my $records = 0;
my $outputdata = "";

### Connect to DB
use DBI;
$dbh=DBI->connect($DSN,$username,$password);

print "$DSN, $username, $password, $tablename, $inputfile<br>";


open(INF,"$inputfile");
  @filearray = <INF>;
close(INF);
chomp($filearray[0]);
@fieldnames = split(/¦/, $filearray[0]);
shift (@filearray);

### Construct insert SQL using $tablename and @fieldnames
my $sql="INSERT INTO $tablename(";
my $sql2;
my $field;
my $arrayindex = 0;
my $ignorenumber = -1;
foreach $field (@fieldnames) {
  if ($field eq $ignorefield) {
    $ignorenumber = $arrayindex;
  } ## End if
  else {
    $sql .= "$field,";
    $sql2 .= "?,";
  } ## End unless
  $arrayindex++;
} ## End loop
chop $sql;
chop $sql2;
$sql .= ")values($sql2)";

print "SQL - $sql<br>";

my $record;
foreach $record (@filearray) {
  chomp($record);
  @fieldvalues = split(/¦/, $record);
  if ($record =~ /¦$/) {
    $fieldnum = @fieldvalues;
    $fieldvalues[$fieldnum] = "";
  } ## End if
  my $sth=$dbh->prepare($sql);
  my @newfieldarray;
  my $arrayindex = 0;
  foreach $field (@fieldvalues) {
    unless ($arrayindex == $ignorenumber) {
      push(@newfieldarray, $field);
    } ## End if
    $arrayindex++;
  } ## End loop
  $sth->execute(@newfieldarray) or print "Cannot insert fields: $DBI::errstr\n";
} ## End loop

$dbh->disconnect();

my @return = $records;
return @return;

} ## End if


##################################################
################### Get Any Cookie
##################################################

sub GetAnyCookie {
### Gets any cookie
my $cookievalue = '';

$cdata = $ENV{'HTTP_COOKIE'};
if ($cdata =~ /\;/) {
  @cookies = split(/; /,$cdata);
  foreach $i (@cookies) {
    ($name,$cid) = split(/=/,$i);
    if ($name eq $_[0]) {
	$cookievalue = $cid;
    } ## End if
  } ## End loop
} ## End If
else {
  ($name,$cid) = split(/=/,$cdata);
  if ($name eq $_[0]) {
    $cookievalue = $cid;
  } ## End if
} ## End else

return $cookievalue;

} ## End sub


##################################################
######################## Session manager
##################################################

sub GetSession {
## Simple session management
my ($id, $pathtosessions, $stimeout, $username, $password) = @_;
return 0 unless ($id);
my $ip=$ENV{'REMOTE_ADDR'};
my (@sessions,%sessions,$session,$found,$time,$logout);
$time=time;
$found=0;
$logout = 0;
if ($stimeout =~ /logout/gis) {
  $stimeout =~ s/logout//gis;
  $logout = 1;
} ## End if
open INF,"$pathtosessions/sessions";
  @sessions=<INF>;
close INF;
foreach $line (@sessions){
  chomp $line;
  ($session{'id'},$session{'ip'},$session{'name'},$session{'pass'},$session{'time'})=split(/¦/,$line);
  if (($time - $session{'time'})>$stimeout){
    undef $line;
    next;
  } ## End if
  if ($logout && $id eq $session{'id'}) {
    undef $line;
    next;
  } ## End if
  if ($id eq $session{'id'}){
    $found=1;
    $session{'time'}=$time;
    $line=join ('¦',($session{'id'},$session{'ip'},$session{'name'},$session{'pass'},$session{'time'}));
    $line=$line."\n";
    last;
  } ## End if
  $line=$line."\n";
} ## End loop

$sessions=join('',@sessions);
open OUTF,">$pathtosessions/sessions" or die "!";
  print OUTF $sessions;
close OUTF;
if ($found){
  return %session;
} ## End if
elsif(!$found && $username && $password){
  open OUTF,">>$pathtosessions/sessions";
    print OUTF "$id¦$ip¦$username¦$password¦$time\n";
  close OUTF;
  ($session{'id'},$session{'ip'},$session{'name'},$session{'pass'},$session{'time'})=($id,$ip,$username,$password,$time);
  return %session;
} ## End else

} ## End sub get_session


##################################################
######################## Make zip from directory
##################################################

sub MakeZipFromDir {
## Simple zip creation
my ($outzipfilename, $sourcedir, $outputfolder, $compression, %SWAPLIST) = @_;
my $zip = Archive::Zip->new();
my $member = $zip->addDirectory( '/' );
#$member = $zip->addString( 'This is a test', 'stringMember.txt' );
$member->desiredCompressionMethod( COMPRESSION_DEFLATED );
$member->desiredCompressionLevel($compression);

## Read source directory
opendir(DIR, "$sourcedir");
  @sourcefiles = readdir(DIR);
closedir(DIR);
foreach $file (@sourcefiles) {
  chomp($file);
  unless ($file eq "." || $file eq ".." || $file =~ /.tmpfile$/ || -d "$sourcedir/$file") {
    $fileto = "$sourcedir/$file.tmpfile";
    &CommonSub::TemplateParseAndWrite("$sourcedir/$file","$fileto",%SWAPLIST);
    if (-B "$sourcedir/$file") {
      $member = $zip->addFile( $fileto, $file );
    } ## End if
    else {
      $writecontent = &ReadFileAsString($fileto);
      $member = $zip->addString( $writecontent, $file );
      $member->desiredCompressionLevel($compression);
    } ## End else
  } ## End unless
} ## End loop

$outzipfilename = "$outputfolder/$outzipfilename";

if ($zip->writeToFileNamed( $outzipfilename ) == AZ_OK) {
  return 1;
} ## End if
else {
  return 0;
} ## End else

} ## End sub


##################################################
######################## Load Module
##################################################

sub LoadModule {
our $module = $_[0];
my $loadok = 1;
package main;
eval "require $module";
if ($@) {
  package CommonSub;
  $loadok = 0;
  package main;
} ## End if
else {
  $module->import(@_[1 .. $#_]);
} ## End else
package CommonSub;
return $loadok;

} ## End sub


##################################################
######################## Check for module
##################################################

sub CheckForModule {
## Check for a module
my $modulename = $_[0];
my $modulefound = 0;
$modulename =~ s/::/\//gis;
foreach $modulepath (@INC) {
  if (-e "$modulepath/$modulename.pm") {
    $modulefound = 1;
  } ## End if
} ## End loop

return $modulefound;

} ## End sub


##################################################
######################## Check for module Long
##################################################

sub CheckForModuleLong {
## Check for a module
my $modulename = $_[0];
my $modulefound = 0;
my @directories;
my @variables;
my $directoryname = 1;
push (@directories,@INC);

@modulenames = split(/::/, $modulename);

until ($directoryname eq "") {
  $directoryname = shift (@directories);
  chomp($directoryname);
  opendir(CURRENTDIR, "$directoryname");
    @dirfiles = readdir(CURRENTDIR);
  closedir(CURRENTDIR);
  foreach $filename (@dirfiles) {
    chomp($filename);
    unless ($filename eq "." || $filename eq "..") {
      if (-d "$directoryname/$filename") {
        push (@directories,"$directoryname/$filename");
      } ## End if
      if ($#modulenames == 2) {
        while ($directoryname =~ /\//g) {
          $folder = $';
        } ## End loop
        while ($` =~ /\//g) {
          $folder2 = $';
        } ## End loop
        if ($filename eq $modulenames[2] && $folder eq $modulenames[1] && $folder2 eq $modulenames[0]) {
          $modulefound = 1;
        } ## End if
      } ## End if
      elsif ($#modulenames == 1) {
        while ($directoryname =~ /\//g) {
          $folder = $';
        } ## End loop
        if ($filename eq $modulenames[1] && $folder eq $modulenames[0]) {
          $modulefound = 1;
        } ## End if
      } ## End if
      else {
        if ($filename eq $modulenames[$#modulenames]) {
          $modulefound = 1;
        } ## End if
      } ## End else
    } ## End unless
  } ## End loop
} ## End loop

return $modulefound;

} ## End sub















1;




