#
# This is the name of the current module.
#
package SendMail;

#===============================================================================
#
# Constructor: 
#	$obj = new SendMail;
#       $obj = new SendMail($smtpserver);
#       $obj = new SendMail($smtpserver, $smtpport);
#
# Methods:
# 	$obj->Bcc($bccemailadd1, [$bccemailadd2, ...]);
# 	$obj->Cc($ccemailadd1, [$ccemailadd2, ...]);
# 	$obj->ErrorsTo($errorstoadd1, [$errorstoadd2, ...]);
# 	$obj->From($sender);
# 	$obj->OFF;
# 	$obj->ON;
# 	$obj->ReplyTo($replytoadd1, [$replytoadd2, ...]);
# 	$obj->Subject($subject);
# 	$obj->To($recipient1, [$recipient2, ...]);
# 	$obj->createMailData();
# 	$obj->getEmailAddress($emailaddstr);
# 	$obj->getRcptLists();
# 	$obj->isMailReady();
#	$obj->receiveFromServer(\*SOCKET);
# 	$obj->reset();
# 	$obj->sendMail();
#	$obj->sendToServer(\*SOCKET, $message);
# 	$obj->setDebug($obj->ON);
# 	$obj->setError($errormessage);
# 	$obj->setMailBody($mailbody);
# 	$obj->setMailHeader($mailheader, $mailheadervalue);
# 	$obj->setSMTPPort($smtpport);
# 	$obj->setSMTPServer($smtpserver);
# 	$obj->version;
#
# *p/s: For more details, please refer to the description below.
#
#===============================================================================

#
# We are using Socket.pm to connect to the SMTP port.
#
use Socket;

use strict;
use vars qw($LOCALHOST $VERSION $MAILER);

#
# Some of the SMTP server needs to say "HELO domain.address".
#
use Sys::Hostname;
$LOCALHOST = hostname;

$VERSION = "1.08";
$MAILER  = "Perl SendMail Module";

#===============================================================================
#
# CONSTRUCTOR:	$obj = new SendMail;
#		$obj = new SendMail($smtpserver);
#		$obj = new SendMail($smtpserver, $smtpport);
#
# DESCRIPTION:	This is the constructor of the SendMail object.
#
#===============================================================================
sub new {
    my($pkg) 		= shift;
    my($smtpserver) 	= shift;
    my($smtpport) 	= shift;
    my($self) 		= {};

    bless $self, $pkg;

    #
    # The mail server.
    #
    $self->{'smtpserver'}  = ($smtpserver && $smtpserver =~ /^\s*$/)
	 ? "localhost" : $smtpserver;

    #
    # The port number for smtp.
    #
    $self->{'smtpport'}    = ($smtpport && $smtpport =~ /^\d+$/) ? $smtpport : 25;

    #
    # The default debug mode is "OFF".
    #
    $self->{'debugmode'}   = $self->OFF;

    #
    # Set the default mailer.
    #
    $self->setMailHeader("X-MAILER", "$MAILER $VERSION");

    return $self;

}

#===============================================================================
#
# METHOD:	$obj->Bcc($bccemailadd1, [$bccemailadd2, ...]);
#
# DESCRIPTION:	Add a list of the name/email address to the blind carbon copy 
#		list.
#
#===============================================================================
sub Bcc {
    my($self)      = shift;
    my(@bcc)       = @_;
    my($currEmail) = undef;

    for $currEmail (@bcc) {
      push(@{$self->{'mailheaders'}->{'BCC'}}, $currEmail) if 
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->Cc($ccemailadd1, [$ccemailadd2, ...]);
#
# DESCRIPTION:	Add a list of the name/email address to the carbon copy list.
#
#===============================================================================
sub Cc {
    my($self)      = shift;
    my(@cc)        = @_;
    my($currEmail) = undef;

    for $currEmail (@cc) {
      push(@{$self->{'mailheaders'}->{'CC'}}, $currEmail) if 
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->ErrorsTo($errorstoadd1, [$errorstoadd2, ...]);
#
# DESCRIPTION:	Add a list of the name/email address into the "Errors-To" list.
#
#===============================================================================
sub ErrorsTo {
    my($self)      = shift;
    my(@errorsto)  = @_;
    my($currEmail) = undef;

    for $currEmail (@errorsto) {
      push(@{$self->{'mailheaders'}->{'ERRORS-TO'}}, $currEmail) if
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->From($sender);
#
# DESCRIPTION:	Set the sender of the email.
#
#===============================================================================
sub From {
    my($self) = shift;
    my($from) = shift;

    $self->{'mailheaders'}->{'FROM'} = $from;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->OFF;
#
# DESCRIPTION:	Will return 0. Basically, it is used to set the debug mode OFF.
#		Eg. $obj->setDebug($obj->OFF);
#
#===============================================================================
sub OFF {
    my($self) = shift;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->ON;
#
# DESCRIPTION:	Will return 1. Basically, it is used to set the debug mode ON.
#		Eg. $obj->setDebug($obj->ON);
#
#===============================================================================
sub ON {
    my($self) = shift;

    return 1;
}

#===============================================================================
#
# METHOD:	$obj->ReplyTo($replytoadd1, [$replytoadd2, ...]);
#
# DESCRIPTION:	Add a list of the name/email address into the "Reply-To" list.
#
#===============================================================================
sub ReplyTo {
    my($self)      = shift;
    my(@replyto)   = @_;

    push(@{$self->{'mailheaders'}->{'REPLY-TO'}}, @replyto);

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->Subject($subject);
#
# DESCRIPTION:	Set the subject of the email.
#
#===============================================================================
sub Subject {
    my($self)	 = shift;
    my($subject) = shift;

    $self->{'mailheaders'}->{'SUBJECT'} = $subject;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->To($recipient1, [$recipient2, ...]);
#
# DESCRIPTION:	Add a list of the name/email address to the recipient list.
#
#===============================================================================
sub To {
    my($self)      = shift;
    my(@to)        = @_;
    my($currEmail) = undef;
    
    for $currEmail (@to) {
      push(@{$self->{'mailheaders'}->{'TO'}}, $currEmail) if 
		($self->getEmailAddress($currEmail) !~ /^\s*$/);
    }

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->createMailData();
#
# DESCRIPTION:	This method will create the mail data which will be sent to the
#		SMTP server. It will contain some mail headers and mail body.
#
#===============================================================================
sub createMailData {
    my($self) = shift;
    my($currHeader) = undef;

    return -1 if $self->isMailReady() != 0;

    $self->{'maildata'} = undef;

    $self->{'maildata'} = "To: ";
    $self->{'maildata'} .= join(",\n\t", @{$self->{'mailheaders'}->{'TO'}});
    $self->{'maildata'} .= "\nFrom: ".$self->{'mailheaders'}->{'FROM'}."\n";
    $self->{'maildata'} .= "Subject: ".$self->{'mailheaders'}->{'SUBJECT'}."\n";
    if (defined $self->{'mailheaders'}->{'CC'} && 
		@{$self->{'mailheaders'}->{'CC'}} > 0) {
      $self->{'maildata'} .= "Cc: ";
      $self->{'maildata'} .= join(",\n\t", @{$self->{'mailheaders'}->{'CC'}});
      $self->{'maildata'} .= "\n";
    }

    if (defined $self->{'mailheaders'}->{'REPLY-TO'} && 
		@{$self->{'mailheaders'}->{'REPLY-TO'}} > 0) {
      $self->{'maildata'} .= "Reply-To: ";
      $self->{'maildata'} .= join(",\n\t", 
		@{$self->{'mailheaders'}->{'REPLY-TO'}})."\n";
    }

    if (defined $self->{'mailheaders'}->{'ERRORS-TO'} && 
		@{$self->{'mailheaders'}->{'ERRORS-TO'}} > 0) {
      $self->{'maildata'} .= "Errors-To: ";
      $self->{'maildata'} .= join(",\n\t", 
		@{$self->{'mailheaders'}->{'ERRORS-TO'}})."\n";
    }

    for $currHeader (sort keys %{$self->{'mailheaders'}->{'OTHERS'}}) {
      my($currMailHeader) = undef;
      ($currMailHeader = $currHeader) =~ s/\b(\w)(\w+)\b/$1\L$2/g;
      $self->{'maildata'} .= "$currMailHeader: ";
      $self->{'maildata'} .= $self->{'mailheaders'}->{'OTHERS'}->{$currHeader};
      $self->{'maildata'} .= "\n";
    }

    $self->{'maildata'} .= "\n";

    $self->{'maildata'} .= "$self->{'mailbody'}\n";

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->getEmailAddress($emailaddstr);
#
# DESCRIPTION:	Get the email address from the email address string which might
#		contain email account owner's name, what we want is the email 
#		address only.
#
#===============================================================================
sub getEmailAddress {
    my($self)  = shift;
    my($value) = shift;
    my($retvalue) = undef;

    if ($value =~ /^\<([^\>\@]+\@[\w\-]+(\.[\w\-]+)+)\>/) {
      ($retvalue = $1) =~ tr/[A-Z]/[a-z]/;
      return $retvalue;
    }

    if ($value =~ /^[^\<]+\<([^\>\@]+\@[\w\-]+(\.[\w\-]+)+)\>/) {
      ($retvalue = $1) =~ tr/[A-Z]/[a-z]/;
      return $retvalue;
    }

    return "" if $value =~ /\s+/;

    $value =~ tr/[A-Z]/[a-z]/;
    return $value if $value =~ /^[^\@]+\@[\w\-]+(\.[\w\-]+)+$/;

    return "";
}

#===============================================================================
#
# METHOD:	$obj->getRcptLists();
#
# DESCRIPTION:	This will generate an array of the recipients' email address.
#		Basically, this method only called by $obj->sendMail() method, 
#		which needs to send "RCPT TO:" request to the SMTP server.
#
#===============================================================================
sub getRcptLists {
    my($self) = shift;
    my(@rcptLists) = ();
    my($currEmail) = undef;

    for $currEmail (@{$self->{'mailheaders'}->{'TO'}}) {
      my($currEmail) = $self->getEmailAddress($currEmail);
      push(@rcptLists, $currEmail) if 
		($currEmail !~ /^\s*$/ && (! grep(/^$currEmail$/, @rcptLists)));
    }

    if (defined $self->{'mailheaders'}->{'BCC'} && 
		@{$self->{'mailheaders'}->{'BCC'}} > 0) {
      for $currEmail (@{$self->{'mailheaders'}->{'BCC'}}) {
        my($currEmail) = $self->getEmailAddress($currEmail);
        push(@rcptLists, $currEmail) if 
		($currEmail !~ /^\s*$/ && (! grep(/^$currEmail$/, @rcptLists)));
      }
    }

    if (defined $self->{'mailheaders'}->{'CC'} && 
		@{$self->{'mailheaders'}->{'CC'}} > 0) {
      for $currEmail (@{$self->{'mailheaders'}->{'CC'}}) {
        my($currEmail) = $self->getEmailAddress($currEmail);
        push(@rcptLists, $currEmail) if 
		($currEmail !~ /^\s*$/ && (! grep(/^$currEmail$/, @rcptLists)));
      }
    }

    return \@rcptLists;
}

#===============================================================================
#
# METHOD:	$obj->isMailReady();
#
# DESCRIPTION:	Check if the basic mail headers and the mail body have been set 
#		or not.
#		p/s: The "From:", "To:" and "Subject:" mail headers are required
#		here, I feel that a mail should contain these headers. It is 
#		just a personal opinion, if you do not think so, just comment 
#		them out.
#
#===============================================================================
sub isMailReady {
    my($self) = shift;

    return $self->setError("No sender has been specified.") if
	! defined $self->{'mailheaders'}->{'FROM'};

    return $self->setError("No recipient has been specified.") if 
	((! defined $self->{'mailheaders'}->{'TO'}) ||
		(defined @{$self->{'mailheaders'}->{'TO'}} &&
		 @{$self->{'mailheaders'}->{'TO'}} < 1));

    return $self->setError("No subject has been specified.") if
	! defined $self->{'mailheaders'}->{'SUBJECT'};

    return $self->setError("No mail body has been set.") if
	! defined $self->{'mailbody'};

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->receiveFromServer(\*SOCKET);
#
# DESCRIPTION:	This will receive the data replied from the server.
#
#===============================================================================
sub receiveFromServer {
    my($self) = shift;
    my($socket) = shift;
    my($reply);

    #
    # We keep receiveing the data from the server until
    # it waits for next command.
    #
    while ($socket && ($reply = <$socket>)) {
      return $self->setError($reply) if $reply =~ /^5/;
      print $reply if $self->{'debugmode'};
      last if $reply =~ /^\d+ /;
    }

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->reset();
#
# DESCRIPTION:	This will clear the data that have been set before.
#
#===============================================================================
sub reset {
    my($self) = shift;

    $self->{'debugmode'} = $self->OFF;
    $self->{'mailbody'} = undef;
    $self->{'maildata'} = undef;
    $self->{'mailheaders'} = undef;
    $self->{'sender'} = undef;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->sendMail();
#
# DESCRIPTION:	This will use the Socket to connect to the SMTP port to send the#		mail.
#
#===============================================================================
sub sendMail {
    my($self) = shift;
    my($iaddr, $paddr, $proto, $rcptlistRef, $currEmail) = undef;

    #
    # Get the sender's email address, this will be used in "MAIL FROM:" request.
    #
    $self->{'sender'} = $self->getEmailAddress($self->{'mailheaders'}->{'FROM'});

    #
    # Invalid email address format.
    #
    return $self->setError("Please check the sender's email address setting.")
	if $self->{'sender'} =~ /^\s*$/; 

    #
    # We create the mail data here.
    #
    return -1 if $self->createMailData() != 0;

    #
    # We get the recipients' email addresses.
    #
    $rcptlistRef = $self->getRcptLists();

    #
    # If no recipient has been specified, this is an error.
    #
    return $self->setError("No recipient has been specified.") if 
		@{$rcptlistRef} == 0;

    #
    # Please refer to Socket module manual. (perldoc Socket)
    #
    $iaddr = inet_aton($self->{'smtpserver'}) || 
		return $self->setError("no host: $self->{'smtpserver'}");
    $paddr = sockaddr_in($self->{'smtpport'}, $iaddr);
    $proto = getprotobyname('tcp');
    socket(SOCK, PF_INET, SOCK_STREAM, $proto) || 
		return $self->setError("Socket error: $!");
    connect(SOCK, $paddr) || 
	return $self->setError("Error in connecting to $self->{'smtpserver'} at port $self->{'smtpport'}: $!");

    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "HELO $LOCALHOST") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "MAIL FROM: <$self->{'sender'}>") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    for $currEmail (@{$rcptlistRef}) {
      return -1 if $self->sendToServer(\*SOCK, "RCPT TO: <$currEmail>") != 0;
      return -1 if $self->receiveFromServer(\*SOCK) != 0;
    }
    return -1 if $self->sendToServer(\*SOCK, "DATA") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "$self->{'maildata'}\r\n.") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    return -1 if $self->sendToServer(\*SOCK, "QUIT") != 0;
    return -1 if $self->receiveFromServer(\*SOCK) != 0;
    eof(SOCK) || close(SOCK) || return $self->setError("Fail close connectiong socket: $!");
    print "The mail has been sent to ".scalar(@{$rcptlistRef}) if 
		$self->{'debugmode'};
    print " person/s successfully.\n" if $self->{'debugmode'};

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->sendToServer(\*SOCKET, $message);
#
# DESCRIPTION:	This will send the message to the SMTP server.
#
#===============================================================================
sub sendToServer {
    my($self) = shift;
    my($socket) = shift;
    my($message) = shift;

    print "$message\n" if $self->{'debugmode'};

    #
    # Sending data to the server.
    #
    send($socket, "$message\r\n", 0) || 
		return $self->setError("Fail to send $message: $!");

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->setDebug($obj->ON);
#		$obj->setDebug($obj->OFF);
#
# DESCRIPTION:	Set the debug mode as ON/OFF.
#		Also see: $obj->ON and $obj->OFF methods.
#
#===============================================================================
sub setDebug {
    my($self) = shift;
    my($flag) = shift;

    $self->{'debugmode'} = $flag;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->setError($errormessage);
#
# DESCRIPTION:	This will set the error message to "error" attribute in the 
#		object and return -1 value.
#
#===============================================================================
sub setError {
    my($self)     = shift;
    my($errorMsg) = shift;

    $self->{'error'} = $errorMsg if $errorMsg !~ /^\s*$/;

    return -1;
}

#===============================================================================
#
# METHOD:	$obj->setMailBody($mailbody);
#
# DESCRIPTION:	Set the mail body content.
#
#===============================================================================
sub setMailBody {
    my($self)	  = shift;
    my($mailbody) = shift;

    $self->{'mailbody'} = $mailbody;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->setMailHeader($mailheader, $mailheadervalue);
#
# DESCRIPTION:	This method is used for setting custom email headers.
#
#===============================================================================
sub setMailHeader {
    my($self)	  	 = shift;
    my($mailheader)	 = shift;
    my($mailheadervalue) = shift;

    $mailheader =~ tr/[a-z]/[A-Z]/;

    $self->{'mailheaders'}->{'OTHERS'}->{$mailheader} = $mailheadervalue;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->setSMTPPort($smtpport);
#
# DESCRIPTION:	Set the SMTP port.
#
#===============================================================================
sub setSMTPPort {
    my($self)     = shift;
    my($smtpport) = shift;

    $self->{'smtpport'} = $smtpport if $smtpport =~ /^\d+$/;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->setSMTPServer($smtpserver);
#
# DESCRIPTION:	Set the SMTP server.
#
#===============================================================================
sub setSMTPServer {
    my($self)       = shift;
    my($smtpserver) = shift;

    $smtpserver =~ s/\s*//g;

    $self->{'smtpserver'} = $smtpserver if $smtpserver !~ /^\s*$/;

    return 0;
}

#===============================================================================
#
# METHOD:	$obj->version;
#
# DESCRIPTION:	Get the version of the module.
#
#===============================================================================
sub version {
    my($self) = shift;

    return $VERSION;
}

1;
#===============================================================================
#
# END of the module.
#
#===============================================================================
__END__

=head1 NAME

SendMail -- This is a perl module which is using Socket to connect the SMTP port to send mails.

=head1 SYNOPSIS

  use SendMail;

  $smtpserver 		= "mail.server.com";
  $smtpport   		= 25;
  $sender     		= "Sender <sender@domain.com>";
  $subject    		= "Subject of the mail.";
  $recipient  		= "Recipient <recipient@domain.com>";
  $recipient2 		= "Recipient 2 <recipient2@domain.com>";
  @recipients 		= ($recipient, $recipient2);
  $administrator 	= "Administrator <admin@domain.com>";
  $administrator2 	= "Administrator 2 <admin2@domain.com>";
  $replyto		= $sender;
  $replyto2		= $recipient;
  @replytos		= ($replyto, $replyto2);
  $header		= "X-Mailer";
  $headervalue		= "Perl SendMail Module 1.08";
  $mailbodydata		= "This is a testing mail.";

  $obj = new SendMail();
  $obj = new SendMail($smtpserver);
  $obj = new SendMail($smtpserver, $smtpport);

  $obj->setDebug($obj->ON);
  $obj->setDebug($obj->OFF);

  $obj->From($sender);

  $obj->Subject($subject);

  $obj->To($recipient);
  $obj->To($recipient, $recipient2);
  $obj->To(@recipients);

  $obj->Cc($recipient);
  $obj->Cc($recipient, $recipient2);
  $obj->Cc(@recipients);

  $obj->Bcc($recipient);
  $obj->Bcc($recipient, $recipient2);
  $obj->Bcc(@recipients);

  $obj->ErrorsTo($administrator);
  $obj->ErrorsTo($administrator, $administrator2);
  $obj->ErrorsTo(@administrators);

  $obj->ReplyTo($replyto);
  $obj->ReplyTo($replyto, $replyto2);
  $obj->ReplyTo(@replytos);

  $obj->setMailHeader($header, $headervalue);

  $obj->setMailBody($mailbodydata);

  if ($obj->sendMail() != 0) {
    print $obj->{'error'}."\n";
  }

  $obj->reset();

=head1 EXAMPLE


http://www.tneoh.zoneit.com/perl/SendMail/testSendMail.pl

=head1 DESCRIPTION


This module is written so that user can easily use it to send mailing list. 
Please do not abuse it.

And it can be used in any perl script to send a mail similar to sending mail
by using /usr/lib/sendmail program.

I have tested this module on Unix and Windows platforms, it works fine. 
Of course you need perl version 5. With the example script, 
testSendMail.pl, you can simply a testing on it.

Errors, comments or questions are welcome.

=head1 CHANGES


1.00->1.01 Recipients with email address contains a "-" in the hostname,
will be able to receive the email now.

1.01->1.02 Module now not only expecting one line reply from the server, it
can receive multiple lines until the server waiting for next command.

1.02->1.03 Repeat declaration of "$currEmail" will give an error in NT
system.

1.03->1.04 Email addresses are enclosed in < and > after "MAIL FROM" and
"RCPT TO" commands.(RFC821) For Microsoft Exchange 4, email addresses
not enclosed in < and > will get an error from the system.

1.04->1.05 getEmailAddress() subroutine should accept email address
in just "<user@domain.com>" format.

1.05->1.06 sendToServer() subroutine should send "\r\n" instead of
"\n" only to the server. Sending only "\n" to the SMTP server, will
cause errors for SMTP server on Windows platform.

1.06->1.07 Calling eof() to check the opened socket, else it will
cause an error in ActivePerl5.6.

1.07->1.08 After sending the maildata, supposed to be "\r\n" instead
of just "\n".

=head1 CREDITS


laurens van alphen 

Dag Øien 

Juliano, Sylvia, CON, OASD(HA)/TMA 

Arjan Woerden

Jeff Graves

=head1 SOURCE


http://www.tneoh.zoneit.com/perl/SendMail/download/


=head1 AUTHOR


Simon Tneoh Chee-Boon	tneohcb@pc.jaring.my

Copyright (c) 1998,1999,2000 Simon Tneoh Chee-Boon. All rights reserved.
This program is free software; you can redistribute it and/or
modify it under the same terms as Perl itself.

=head1 VERSION

Version 1.08 	15 August 2000

=head1 SEE ALSO

Socket.pm

=cut
