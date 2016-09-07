

BEGIN{
    olddate="1970-01-01"
    total = 0;
    #edition
    atomic=0;
    cloud=0;
    server=0;
    workstation=0;
    edit=0;
    unk_edt=0;
    # release
    f20=0;
    f21=0;
    f22=0;
    f23=0;
    f24=0;
    f25=0;
    f26=0;
    f27=0;
    f28=0;
    f29=0;
    unk_rel=0;
    # arch
    arm_32=0;
    arm_64=0;
    x86_32=0;
    x86_64=0;
    ppc_le=0;
    ppc_he=0;
    s390x=0;
    unk_arc=0;
    # spins 
    spin = 0;
    xfce = 0;
    soas = 0;
    lxde = 0;
    secu = 0;
    robo = 0;
    mate = 0;
    scik = 0;
    jamk = 0;
    desi = 0;
    elec = 0;
    game = 0;
    mini = 0;
    cinn = 0;
    kde = 0;
    # additional data
    netinstall=0;
    netserv=0;
    network=0;
    netclod=0;
    print olddate ",02-total,03-editions,04-atomic,05-cloud,06-server,07-workstation,08-unk_edition,09-f20,10-f21,11-f22,12-f23,13-f24,14-f25,15-f26,16-f27,17-f28,18-f29,19-unk_rel,20-arm_32,21-arm_64,22-ppc_le,23-ppc_he,24-s390x,25-x86_32,26-x86_64,27-unk_arc,28-netinstall,29-netserv,30-network,31-netclod,32-spin,33-Xfce,34-SoaS,35-LXDE,36-Security,37-Robotics,38-Mate,39-Scientific,40-Jam,41-Design,42-Electronics,43-Games,44-Minimal,45-Cinnamon,46-KDE"
    olddate="1970-01-02";
}

{
    if ($1 == olddate) {
      if (($3 ~/\.x86_64\./) || ($3 ~/-x86_64-/)) { x86_64 = x86_64 +1; }
      else if (($3 ~/\.i686\./) || ($3 ~/-i686-/) || ($3 ~/\.i386\./) || ($3 ~/-i386-/)) { x86_32 = x86_32 +1; }
      else if (($3 ~/\.armhfp\./) || ($3 ~/-armhfp-/)){ arm_32 = arm_32 +1; }
      else if (($3 ~/\.aarch64\./) || ($3 ~/-aarch64-/)){ arm_64= arm_64 +1; }
      else if (($3 ~/\.ppc64le\./) || ($3 ~/-ppc64le-/)){ ppc_le = ppc_le +1; }
      else if (($3 ~/\.ppc64\./) || ($3 ~/-ppc64-/)){ ppc_he = ppc_he +1; }
      else if (($3 ~/\.s390x\./) || ($3 ~/-s390x-/)){ s390x = s390x +1; }
      else { unk_arc = unk_arc +1 };

      if (($3 ~/-20\./) || ($3 ~/-20-/)) { f20 = f20 + 1 }
      else if (($3 ~/-21\./) || ($3 ~/-21-/)) { f21 = f21 + 1 }
      else if (($3 ~/-22\./) || ($3 ~/-22-/)) { f22 = f22 + 1 }
      else if (($3 ~/-23\./) || ($3 ~/-23-/)) { f23 = f23 + 1 }
      else if (($3 ~/-24\./) || ($3 ~/-24-/)) { f24 = f24 + 1 }
      else if (($3 ~/-25\./) || ($3 ~/-25-/)) { f25 = f25 + 1 }
      else if (($3 ~/-26\./) || ($3 ~/-26-/)) { f26 = f26 + 1 }
      else if (($3 ~/-27\./) || ($3 ~/-27-/)) { f27 = f27 + 1 }
      else if (($3 ~/-28\./) || ($3 ~/-28-/)) { f28 = f28 + 1 }
      else if (($3 ~/-29\./) || ($3 ~/-29-/)) { f29 = f29 + 1 }
      else {unk_rel = unk_rel +1 }

      if (($3 ~/Cloud-Atomic/) || ($3 ~/Cloud_Atomic/) || ($3 ~/Fedora-Atomic/) )   { atomic = atomic +1 ; edit = edit +1; total = total +1 }
      else if (($3 ~/Cloud-Base/) || ($3 ~/Cloud_Base/))            { cloud = cloud +1 ; edit = edit +1; total = total +1 }
      else if (($3 ~/Cloud-netinst/) || ($3 ~/Cloud_netinst/))      { cloud = cloud +1; netinstall = netinstall +1 ; netclod=netclod+1; edit = edit +1; total = total +1 }
      else if (($3 ~/Server-DVD/) || ($3 ~/Server_DVD/) || ($3 ~/Server-dvd/))                   { server = server +1; edit = edit +1;total = total +1 }
      else if (($3 ~/Server-netinst/) || ($3 ~/Server_netinst/))    { server = server +1; netinstall = netinstall +1 ; netserv=netserv+1; edit = edit +1;total = total +1 }
      else if (($3 ~/Workstation-netinst/) || ($3 ~/Workstation_netinst/)) { workstation = workstation +1; netinstall = netinstall +1; network=network+1; edit = edit +1;total = total +1 }
      else if (($3 ~/Live-Workstation/) || ($3 ~/Live_Workstation/)  || ($3 ~/Workstation-Live/))       { workstation = workstation +1; edit = edit +1;total = total +1 }
      else if (($3 ~/Desktop/) || ($3 ~/Desktop/))       { workstation = workstation +1; edit = edit +1;total = total +1 }
      else if (($3 ~/Fedora-20-i386-DVD/) || ($3 ~/Fedora-20-ppc64-DVD/) || ($3 ~/Fedora-20-x86_64-DVD/) || ($3 ~/Fedora-i386-20/) || ($3 ~/Fedora-x86_64-20/)) { server = server +1; edit = edit +1;total = total +1 }
      else if (($3 ~/Fedora-20-i386-netinst.iso/) || ($3 ~/Fedora-20-ppc64-netinst.iso/) || ($3 ~/Fedora-20-x86_64-netinst.iso/) ) { server = server +1; netinstall = netinstall + 1; netserv = netserv+1; edit = edit +1;total = total +1 }
      else if ($3 ~/Xfce/) { spin = spin +1 ; xfce = xfce +1; total = total + 1}
      else if ($3 ~/SoaS/) { spin = spin +1 ; soas = soas +1; total = total + 1}
      else if ($3 ~/LXDE/) { spin = spin +1 ; lxde = lxde +1; total = total + 1}
      else if ($3 ~/Security/)  { spin = spin +1; secu = secu +1; total = total + 1}
      else if ($3 ~/Robotics/)  { spin = spin +1; robo = robo +1; total = total + 1}
      else if (($3 ~/Mate/) || ($3 ~/MATE/))  { spin = spin +1; mate = mate +1; total = total + 1}
      else if (($3 ~/Scientific_KDE/) || ($3 ~/Scientific-KDE/))  { spin = spin +1; scik = scik +1; total = total + 1}
      else if (($3 ~/Jam_KDE/) || ($3 ~/Jam-KDE/))  { spin = spin +1; jamk = jamk +1; total = total + 1}
      else if (($3 ~/Design_suite/) || ($3 ~/Design-suite/))  { spin = spin +1; desi = desi +1; total = total + 1}
      else if (($3 ~/Electronic_Lab/) || ($3 ~/Electronic-Lab/))  { spin = spin +1; elec = elec +1; total = total + 1}
      else if ($3 ~/Games/)  { spin = spin +1; game = game +1; total = total + 1}
      else if ($3 ~/Minimal/)  { spin = spin +1; mini = mini +1; total = total + 1}
      else if ($3 ~/Cinnamon/)  { spin = spin +1; cinn = cinn +1; total = total + 1}
      else if ($3 ~/KDE/)  { spin = spin +1; kde = kde +1; total = total + 1}
      else { unk_edt = unk_edt + 1; total = total +1} 


    } else {
	if ( olddate !~ "1970-01-01" ) {
	    print olddate "," total "," edit "," atomic "," cloud "," server "," workstation "," unk_edt "," f20 "," f21 "," f22 "," f23 "," f24 "," f25 "," f26 "," f27 "," f28 "," f29 "," unk_rel "," arm_32 "," arm_64 "," ppc_le "," ppc_he "," s390x "," x86_32 "," x86_64 "," unk_arc "," netinstall "," netserv "," network "," netclod "," spin "," xfce "," soas "," lxde ","  secu "," robo "," mate "," scik "," jamk "," desi "," elec "," game "," mini "," cinn "," kde;
	};

	    olddate=$1
	    total = 0;
	    #edition
	    atomic=0;
	    cloud=0;
	    server=0;
	    workstation=0;
	    edit = 0;
	    unk_edt=0;
	    # release
	    f20=0;
	    f21=0;
	    f22=0;
	    f23=0;
	    f24=0;
	    f25=0;
	    f26=0;
	    f27=0;
	    f28=0;
	    f29=0;
	    unk_rel=0;
	    # arch
	    arm_32=0;
	    arm_64=0;
	    x86_32=0;
	    x86_64=0;
	    ppc_le=0;
	    ppc_he=0;
	    s390x=0;
	    unk_arc=0;
	    # spins 
	    spin = 0;
	    xfce = 0;
	    soas = 0;
	    lxde = 0;
	    secu = 0;
	    robo = 0;
	    mate = 0;
	    scik = 0;
	    jamk = 0;
	    desi = 0;
	    elec = 0;
	    game = 0;
	    mini = 0;
	    cinn = 0;
	    kde = 0;
	    # additional data
	    netinstall=0;
	    netserv=0;
	    network=0;
	    netclod=0;
    }
    
}

END {
	    print olddate "," total "," edit "," atomic "," cloud "," server "," workstation "," unk_edt "," f20 "," f21 "," f22 "," f23 "," f24 "," f25 "," f26 "," f27 "," f28 "," f29 "," unk_rel "," arm_32 "," arm_64 "," ppc_le "," ppc_he "," s390x "," x86_32 "," x86_64 "," unk_arc "," netinstall "," netserv "," network "," netclod "," spin "," xfce "," soas "," lxde ","  secu "," robo "," mate "," scik "," jamk "," desi "," elec "," game "," mini "," cinn "," kde;
}

