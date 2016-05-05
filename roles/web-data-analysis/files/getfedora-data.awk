

BEGIN{
    olddate="1970-01-01"
    dt = 0;
    #edition
    atomic=0;
    cloud=0;
    server=0;
    workstation=0;
    unk_edt=0;
    # release
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
    # additional data
    netinstall=0;
    print olddate ",dt,atomic,cloud,server,workstation,unk_edt,f21,f22,f23,f24,f25,f26,f27,f28,f29,unk_rel,arm_32,arm_64,ppc_le,ppc_he,s390x,x86_32,x86_64,unk_arc,netinstall"
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

      if (($3 ~/-21\./) || ($3 ~/-21-/)) { f21 = f21 + 1 }
      else if (($3 ~/-22\./) || ($3 ~/-22-/)) { f22 = f22 + 1 }
      else if (($3 ~/-23\./) || ($3 ~/-23-/)) { f23 = f23 + 1 }
      else if (($3 ~/-24\./) || ($3 ~/-24-/)) { f24 = f24 + 1 }
      else if (($3 ~/-25\./) || ($3 ~/-25-/)) { f25 = f25 + 1 }
      else if (($3 ~/-26\./) || ($3 ~/-26-/)) { f26 = f26 + 1 }
      else if (($3 ~/-27\./) || ($3 ~/-27-/)) { f27 = f27 + 1 }
      else if (($3 ~/-28\./) || ($3 ~/-28-/)) { f28 = f28 + 1 }
      else if (($3 ~/-29\./) || ($3 ~/-29-/)) { f29 = f29 + 1 }
      else {unk_rel = unk_rel +1 }

      if (($3 ~/Cloud-Atomic/) || ($3 ~/Cloud_Atomic/))                    { atomic = atomic +1 ; dt = dt +1 }
      else if (($3 ~/Cloud-Base/) || ($3 ~/Cloud_Base/))                   { cloud = cloud +1 ; dt = dt +1 }
      else if (($3 ~/Server-DVD/) || ($3 ~/Server_DVD/))                   { server = server +1; dt = dt +1 }
      else if (($3 ~/Server-netinst/) || ($3 ~/Server_netinst/))           { server = server +1; netinstall = netinstall +1 ; dt = dt +1 }
      else if (($3 ~/Workstation-netinst/) || ($3 ~/Workstation_netinst/)) { workstation = workstation +1; netinstall = netinstall +1; dt = dt +1 }
      else if (($3 ~/Live-Workstation/) || ($3 ~/Live_Workstation/))       { workstation = workstation +1; dt = dt +1 }
      else { unk_edt = unk_edt + 1; dt = dt +1} 
	  
    } else {
      print olddate "," dt "," atomic "," cloud "," server "," workstation "," unk_edt "," f21 "," f22 "," f23 "," f24 "," f25 "," f26 "," f27 "," f28 "," f29 "," unk_rel "," arm_32 "," arm_64 "," ppc_le "," ppc_he "," s390x "," x86_32 "," x86_64 "," unk_arc "," netinstall
      olddate=$1
      dt = 0;
      #edition
      atomic=0;
      cloud=0;
      server=0;
      workstation=0;
      unk_edt=0;
      # release
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
      # additional data
      netinstall=0;
    }

}

END {
      print olddate "," dt "," atomic "," cloud "," server "," workstation "," unk_edt "," f21 "," f22 "," f23 "," f24 "," f25 "," f26 "," f27 "," f28 "," f29 "," unk_rel "," arm_32 "," arm_64 "," ppc_le "," ppc_he "," s390x "," x86_32 "," x86_64 "," unk_arc "," netinstall
}

