#!/usr/bin/perl
# this scrip query for all running VM and terminate those
# which are not currently started by some ansible script

while (chomp($a = qx(ps ax |grep -v 'sh -c ps ax'  |grep /home/copr/provision/builderpb.yml | grep -v grep))) {
  # we are starting some VM and could not determine correct list of running VMs
  sleep 5;
}

#print qx(ps ax |grep ' 172.16.3.' |awk '{ print \$33 }');
@IPs = split('\s+', qx(ps ax |grep ' 172.16.3.' |awk '{ print \$33 }'));

#print "Running instances\n";
#print join(", ", @IPs), "\n";
for my $i (@IPs) {
  $check{$i} = 1;
}

@instances = split('\n', qx(/bin/euca-describe-instances));
@TO_DELETE = ();
for my $i (@instances) {
  my @COLUMNS = split('\s+', $i);
  next if $COLUMNS[0] eq 'RESERVATION';
  #print $COLUMNS[1], ", ", $COLUMNS[15], "\n";
  push(@TO_DELETE, $COLUMNS[1]) unless $check{$COLUMNS[15]};
}
$id_merged = join(" ", @TO_DELETE);
qx|euca-terminate-instances $id_merged| if ($id_merged);
