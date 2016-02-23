#!/usr/bin/perl
use strict;
my $VERSION = '0.4.5';
my $COPYRIGHT = 'Copyright (C) 2005-2008 Jonathan Buhacoff <jonathan@buhacoff.net>';
my $LICENSE = 'http://www.gnu.org/licenses/gpl.txt';
my %status = ( 'OK' => 0, 'WARNING' => 1, 'CRITICAL' => 2, 'UNKNOWN' => 3 );

# look for required modules
exit $status{UNKNOWN} unless load_modules(qw/Getopt::Long Net::SMTP/);

Getopt::Long::Configure("bundling");
my $verbose = 0;
my $help = "";
my $help_usage = "";
my $show_version = "";
my $smtp_server = "";
my $default_smtp_port = "25";
my $default_smtp_ssl_port = "465";
my $default_smtp_tls_port = "587";
my $smtp_port = "";
my @mailto = ();
my $mailfrom = "";
my @header = ();
my $body = "";
my $stdin = "";
my $expect_response = "250";
my $warntime = 15;
my $criticaltime = 30;
my $timeout = 60;
my $tls = 0;
my $ssl = 0;
my $auth_method = undef;
my $username = "";
my $password = "";
my $ok;
$ok = Getopt::Long::GetOptions(
	"V|version"=>\$show_version,
	"v|verbose+"=>\$verbose,"h|help"=>\$help,"usage"=>\$help_usage,
	"w|warning=i"=>\$warntime,"c|critical=i"=>\$criticaltime,"t|timeout=i"=>\$timeout,
	# smtp settings
	"H|hostname=s"=>\$smtp_server,"p|port=i"=>\$smtp_port,
	"mailto=s"=>\@mailto, "mailfrom=s",\$mailfrom,
	"header=s"=>\@header, "body=s"=>\$body,	"stdin"=>\$stdin,
	# SSL/TLS/auth options
	"tls!"=>\$tls, "ssl!"=>\$ssl, "auth=s"=>\$auth_method,
	"U|username=s"=>\$username,"P|password=s"=>\$password,
	# Server response
	"E|expect-response=s"=>\$expect_response,
	);

if( $show_version ) {
	print "$VERSION\n";
	if( $verbose ) {
		print "Default warning threshold: $warntime seconds\n";
		print "Default critical threshold: $criticaltime seconds\n";
		print "Default timeout: $timeout seconds\n";
	}
	exit $status{UNKNOWN};
}

if( $help ) {
	exec "perldoc", $0 or print "Try `perldoc $0`\n";
	exit $status{UNKNOWN};
}

my @required_module = ();
push @required_module, 'Net::SMTP::SSL' if $ssl;
push @required_module, ('MIME::Base64','Authen::SASL') if $ssl && $username;
push @required_module, 'Net::SMTP::TLS' if $tls;
push @required_module, 'Net::SMTP_auth' if $auth_method;
exit $status{UNKNOWN} unless load_modules(@required_module);


# split up @mailto if commas were used instead of multiple options
@mailto = split(/,/,join(',',@mailto));

if( $help_usage ||
	(
	$smtp_server eq "" || scalar(@mailto)==0 || $mailfrom eq ""
	) 
  ) {
	print "Usage: $0 -H host [-p port] --mailto recipient\@your.net [--mailto recipient2\@your.net ...] --mailfrom sender\@your.net --body 'some text' [-w <seconds>] [-c <seconds>]\n";
	exit $status{UNKNOWN};
}

# initialize
my $report = new PluginReport;
my $time_start = time;
my $actual_response = undef;
my @warning = ();
my @critical = ();


# connect to SMTP server
# create the smtp handle using Net::SMTP, Net::SMTP::SSL, or Net::SMTP::TLS
my $smtp; 
eval {
	if( $tls ) {
		$smtp_port = $default_smtp_tls_port unless $smtp_port;
		$smtp = Net::SMTP::TLS->new($smtp_server, Timeout=>$timeout, Port=>$smtp_port, User=>$username, Password=>$password);
	}
	elsif( $ssl ) {
		$smtp_port = $default_smtp_ssl_port unless $smtp_port;
		$smtp = Net::SMTP::SSL->new($smtp_server, Port => $smtp_port, Timeout=>$timeout,Debug=>0);
		if( $smtp && $username )  {
			$smtp->auth($username, $password);
		}	
	}
	elsif( $auth_method ) {
		$smtp_port = $default_smtp_port unless $smtp_port;
		$smtp = Net::SMTP_auth->new($smtp_server, Port=>$smtp_port, Timeout=>$timeout,Debug=>0);	
		if( $smtp ) {
			$smtp->auth($auth_method, $username, $password);
		}			
	}
	else {
		$smtp_port = $default_smtp_port unless $smtp_port;
		$smtp = Net::SMTP->new($smtp_server, Port=>$smtp_port, Timeout=>$timeout,Debug=>0);	
		if( $smtp && $username ) {
			$smtp->auth($username, $password);
		}	
	}	
};
if( $@ ) {
	$@ =~ s/\n/ /g; # the error message can be multiline but we want our output to be just one line
	print "SMTP SEND CRITICAL - $@\n";
	exit $status{CRITICAL};	
}
unless( $smtp ) {
	print "SMTP SEND CRITICAL - Could not connect to $smtp_server port $smtp_port\n";
	exit $status{CRITICAL};
}
my $time_connected = time;

# add the monitored server's banner to the report
if( $tls ) {
	$report->{banner} = "";	
}
elsif( $ssl ) {
	$report->{banner} = $smtp->banner || "";
	chomp $report->{banner};		
}
else {
	$report->{banner} = $smtp->banner || "";
	chomp $report->{banner};	
}


# send email
if( $stdin ) {
	$body = "";
	while(<STDIN>) {
		$body .= $_;
	}
}
$smtp->mail($mailfrom);
foreach( @mailto ) {
	# the two SMTP modules have different error reporting mechanisms:
	if( $tls ) {
		# Net::SMTP::TLS croaks when the recipient is rejected
		eval {
			$smtp->to($_);			
		};
		if( $@ ) {
			print "SMTP SEND CRITICAL - Could not send to $_\n";
			exit $status{CRITICAL};			
		}
	}
	else {
		# Net::SMTP returns false when the recipient is rejected
		my $to_returned = $smtp->to($_);		
		if( !$to_returned ) { 
			print "SMTP SEND CRITICAL - Could not send to $_\n";
			exit $status{CRITICAL};
		}
	}
}

# Net::SMTP::TLS doesn't implement code() so we need to wrap calls in eval to get our error messages

	# start data transfer (expect response 354)
	$smtp->data();
	
	# send data
	$smtp->datasend("To: ".join(", ",@mailto)."\n");
	$smtp->datasend("From: $mailfrom\n");
	foreach( @header ) {
		$smtp->datasend("$_\n");
	}
	$smtp->datasend("\n");
	$smtp->datasend($body);
	$smtp->datasend("\n");
	
eval {
	# end data transfer (expect response 250)
	$smtp->dataend();	
};
if( $@ ) {
	$actual_response = $tls ? get_tls_error($@) : $smtp->code();
}
else {
	$actual_response = $tls ? "250" : $smtp->code();	# no error means we got 250		
}

eval {
	# disconnect from SMTP server (expect response 221)
	$smtp->quit();
};
if( $@ ) {
	push @warning, "Error while disconnecting from $smtp_server";
}

# calculate elapsed time and issue warnings
my $time_end = time;
my $elapsedtime = $time_end - $time_start;
$report->{seconds} = $elapsedtime;

push @warning, "connection time more than $warntime" if( $time_connected - $time_start > $warntime );
push @critical, "connection time more than $criticaltime" if( $time_connected - $time_start > $criticaltime );
push @critical, "response was $actual_response but expected $expect_response" if ( $actual_response ne $expect_response );

# print report and exit with known status
my $short_report = $report->text(qw/seconds/);
my $long_report = join("", map { "$_: $report->{$_}\n" } qw/banner/ );
if( scalar @critical ) {
	my $crit_alerts = join(", ", @critical);
	print "SMTP SEND CRITICAL - $crit_alerts; $short_report\n";
	print $long_report if $verbose;
	exit $status{CRITICAL};
}
if( scalar @warning ) {
	my $warn_alerts = join(", ", @warning);
	print "SMTP SEND WARNING - $warn_alerts; $short_report\n";
	print $long_report if $verbose;
	exit $status{WARNING};
}
print "SMTP SEND OK - $short_report\n";
print $long_report if $verbose;
exit $status{OK};


# utility to load required modules. exits if unable to load one or more of the modules.
sub load_modules {
	my @missing_modules = ();
	foreach( @_ ) {
		eval "require $_";
		push @missing_modules, $_ if $@;	
	}
	if( @missing_modules ) {
		print "Missing perl modules: @missing_modules\n";
		return 0;
	}
	return 1;
}

# utility to extract error codes out of Net::SMTP::TLS croak messages
sub get_tls_error {
	my ($errormsg) = @_;
	$errormsg =~ m/: (\d+) (.+)/;
	my $code = $1;		
	return $code;
}

# NAME
#	PluginReport
# SYNOPSIS
#	$report = new PluginReport;
#   $report->{label1} = "value1";
#   $report->{label2} = "value2";
#	print $report->text(qw/label1 label2/);
package PluginReport;

sub new {
	my ($proto,%p) = @_;
	my $class = ref($proto) || $proto;
	my $self  = bless {}, $class;
	$self->{$_} = $p{$_} foreach keys %p;
	return $self;
}

sub text {
	my ($self,@labels) = @_;
	my @report = map { "$self->{$_} $_" } grep { defined $self->{$_} } @labels;
	my $text = join(", ", @report);
	return $text;
}

package main;
1;

