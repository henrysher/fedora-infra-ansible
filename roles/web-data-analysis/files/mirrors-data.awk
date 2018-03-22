BEGIN{
    olddate="1970-01-01"
    epel=0;
    fedora=0;
    epel4=0;
    epel5=0;
    epel6=0;
    epel7=0;
    f03=0;
    f04=0;
    f05=0;
    f06=0;
    f07=0;
    f08=0;
    f09=0;
    f10=0;
    f11=0;
    f12=0;
    f13=0;
    f14=0;
    f15=0;
    f16=0;
    f17=0;
    f18=0;
    f19=0;
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
    f30=0;
    rawhide=0;
    rawhide_modular=0;
    modular_f27=0;
    modular_f28=0;
    modular_f29=0;
    modular_f30=0;
    modular=0;
    unknown_release = 0;
    # arch
    alpha=0;
    arm64=0;
    arm=0;
    ia64=0;
    mips=0;
    ppc=0;
    ppc64=0;
    ppc64le=0;
    s390=0;
    sparc=0;
    tilegx=0;
    x86_32=0;
    x86_64=0;
    # sub arch
    ppc_e=0;
    ppc_f=0;
    x86_32_e=0;
    x86_32_f=0;
    x86_64_e = 0;
    x86_64_f = 0;
    unknown_arch = 0;
    centos = 0;
    rhel = 0;
    print olddate ",02-epel4,03-epel5,04-epel6,05-epel7,06-f03,07-f04,08-f05,09-f06,10-f07,11-f08,12-f09,13-f10,14-f11,15-f12,16-f13,17-f14,18-f15,19-f16,20-f17,21-f18,22-f19,23-f20,24-f21,25-f22,26-f23,27-f24,28-f25,29-f26,30-f27,31-f28,32-f29,33-rawhide,34-unk_rel,35-epel,36-fedora,37-alpha,38-arm,39-arm64,40-ia64,41-mips,42-ppc,43-s390,44-sparc,45-tilegx,46-x86_32,47-x86_64,48-x86_32_e,49-x86_32_f,50-x86_64_e,51-x86_64_f,52-ppc_e,53-ppc_f,54-unk_arc,55-centos,56-rhel,57-ppc64,58-ppc64le,59-modular,60-modular_rawhide,61-modular_f27,62-modular_f28,63-modular_f29,64-modular_f30";
    olddate="1970-01-02";
}

{
    if ($1 == olddate) {
	if ($3 ~"epel4")       { epel4=epel4+1; epel=epel+1}
	else if ($3 ~"epel5")  { epel5=epel5+1; epel=epel+1}
	else if ($3 ~"epel6")  { epel6=epel6+1; epel=epel+1}
	else if ($3 ~"epel7")  { epel7=epel7+1; epel=epel+1}
	else if ($3 ~"modular_f27") { modular_f27=modular_f27+1; modular=modular+1; fedora=fedora+1 }
	else if ($3 ~"modular_f28") { modular_f28=modular_f28+1; modular=modular+1; fedora=fedora+1 }
	else if ($3 ~"modular_f29") { modular_f29=modular_f29+1; modular=modular+1; fedora=fedora+1 }
	else if ($3 ~"modular_f30") { modular_f30=modular_f30+1; modular=modular+1; fedora=fedora+1 }
	else if ($3 ~"modular") { modular=modular+1; fedora=fedora+1 }
	else if ($3 ~"f03")     { f03=f03+1; fedora=fedora+1}
	else if ($3 ~"f04")     { f04=f04+1; fedora=fedora+1}
	else if ($3 ~"f05")     { f05=f05+1; fedora=fedora+1}
	else if ($3 ~"f06")     { f06=f06+1; fedora=fedora+1}
	else if ($3 ~"f07")     { f07=f07+1; fedora=fedora+1}
	else if ($3 ~"f08")     { f08=f08+1; fedora=fedora+1}
	else if ($3 ~"f09")     { f09=f09+1; fedora=fedora+1}
	else if ($3 ~"f10")     { f10=f10+1; fedora=fedora+1}
	else if ($3 ~"f11")     { f11=f11+1; fedora=fedora+1}
	else if ($3 ~"f12")     { f12=f12+1; fedora=fedora+1}
	else if ($3 ~"f13")     { f13=f13+1; fedora=fedora+1}
	else if ($3 ~"f14")     { f14=f14+1; fedora=fedora+1}
	else if ($3 ~"f15")     { f15=f15+1; fedora=fedora+1}
	else if ($3 ~"f16")     { f16=f16+1; fedora=fedora+1}
	else if ($3 ~"f17")     { f17=f17+1; fedora=fedora+1}
	else if ($3 ~"f18")     { f18=f18+1; fedora=fedora+1}
	else if ($3 ~"f19")     { f19=f19+1; fedora=fedora+1}
	else if ($3 ~"f20")     { f20=f20+1; fedora=fedora+1}
	else if ($3 ~"f21")     { f21=f21+1; fedora=fedora+1}
	else if ($3 ~"f22")     { f22=f22+1; fedora=fedora+1}
	else if ($3 ~"f23")     { f23=f23+1; fedora=fedora+1}
	else if ($3 ~"f24")     { f24=f24+1; fedora=fedora+1}
	else if ($3 ~"f25")     { f25=f25+1; fedora=fedora+1}
	else if ($3 ~"f26")     { f26=f26+1; fedora=fedora+1}
	else if ($3 ~"f27")     { f27=f27+1; fedora=fedora+1}
	else if ($3 ~"f28")     { f28=f28+1; fedora=fedora+1}
	else if ($3 ~"f29")     { f29=f29+1; fedora=fedora+1}
	else if ($3 ~"f30")     { f30=f30+1; fedora=fedora+1}
	else if ($3 ~"rawhide_modular") { rawhide_modular=rawhide_modular+1; modular=modular+1; fedora=fedora+1}
	else if ($3 ~"rawhide") { rawhide=rawhide+1; fedora=fedora+1}
	else if ($3 ~"centos") { centos=centos+1; epel=epel+1}
	else if ($3 ~"rhel") { rhel=rhel+1; epel=epel+1}
	else                    { unknown_release = unknown_release + 1 ; };
	## ARCH
	if ($4 ~ "arm")        { arm = arm + 1}
	else if ($4 ~ "aarch64")  { arm64 = arm64 +1 }
	else if ($4 ~"ia64")   { ia64 = ia64 + 1}
	else if ($4 ~"mips")   { mips = mips + 1}
	else if ($4 ~"s390")   { s390 = s390 +1 }
	else if ($4 ~"sparc")  { sparc = sparc +1 }
	else if ($4 ~"tilegx") { tilegx = tilegx +1 }
	else if (($4 ~"i386") && ($3 ~"epel"))         { x86_32 = x86_32 + 1; x86_32_e = x86_32_e + 1}
	else if (($4 ~"i386") && ($3 ~/rhel/))         { x86_32 = x86_32 + 1; x86_32_e = x86_32_e + 1}
	else if (($4 ~"i386") && ($3 ~/centos/))       { x86_32 = x86_32 + 1; x86_32_e = x86_32_e + 1}
	else if (($4 ~"i386") && ($3 ~/f[0-2]/))       { x86_32 = x86_32 + 1; x86_32_f = x86_32_f + 1}
	else if (($4 ~"i386") && ($3 ~"rawhide"))      { x86_32 = x86_32 + 1; x86_32_f = x86_32_f + 1}
	else if (($4 ~"x86_64") && ($3 ~"epel"))       { x86_64 = x86_64 + 1; x86_64_e = x86_64_e + 1; }
	else if (($4 ~"x86_64") && ($3 ~/rhel/))       { x86_64 = x86_64 + 1; x86_64_e = x86_64_e + 1; }
	else if (($4 ~"x86_64") && ($3 ~/centos/))     { x86_64 = x86_64 + 1; x86_64_e = x86_64_e + 1; }
	else if (($4 ~"x86_64") && ($3 ~/f[0-2]/))     { x86_64 = x86_64 + 1; x86_64_f = x86_64_f + 1; }
	else if (($4 ~"x86_64") && ($3 ~"rawhide"))    { x86_64 = x86_64 + 1; x86_64_f = x86_64_f + 1; }
	else if (($4 ~"ppc64le") && ($3 ~"epel"))          { ppc64le = ppc64le + 1 ; ppc_e = ppc_e + 1;}
	else if (($4 ~"ppc64le") && ($3 ~/f[0-2]/))        { ppc64le = ppc64le + 1 ; ppc_f = ppc_f + 1;}
	else if (($4 ~"ppc64le") && ($3 ~"rawhide"))       { ppc64le = ppc64le + 1 ; ppc_f = ppc_f + 1;}
	else if (($4 ~"ppc64") && ($3 ~"epel"))          { ppc64 = ppc64 + 1 ; ppc_e = ppc_e + 1;}
	else if (($4 ~"ppc64") && ($3 ~/f[0-2]/))        { ppc64 = ppc64 + 1 ; ppc_f = ppc_f + 1;}
	else if (($4 ~"ppc64") && ($3 ~"rawhide"))       { ppc64 = ppc64 + 1 ; ppc_f = ppc_f + 1;}
	else if (($4 ~"ppc") && ($3 ~"epel"))          { ppc = ppc + 1 ; ppc_e = ppc_e + 1;}
	else if (($4 ~"ppc") && ($3 ~/f[0-2]/))        { ppc = ppc + 1 ; ppc_f = ppc_f + 1;}
	else if (($4 ~"ppc") && ($3 ~"rawhide"))       { ppc = ppc + 1 ; ppc_f = ppc_f + 1;}
	else if ($4 ~/i386/) {x86_32 = x86_32 +1 ; }
	else if ($4 ~/x86_64/) {x86_64 = x86_64 +1; }
	else if ($4 ~/ppc64le/) {ppc64le = ppc64le +1}
	else if ($4 ~/ppc64/) {ppc64 = ppc64 +1}
	else if ($4 ~/ppc/) {ppc = ppc +1}
	else if ($4 ~"mips")   { mips = mips +1 }
	else if ($4 ~"alpha")   { alpha = alpha +1 }
	else                   {unknown_arch = unknown_arch +1; };
    } else {
	if ( olddate !~ "1970-01-01" ) {
	  print olddate "," epel4 "," epel5 "," epel6 "," epel7 "," f03 "," f04 "," f05 "," f06 "," f07 "," f08 "," f09 "," f10 "," f11 "," f12 "," f13 "," f14 "," f15 "," f16 "," f17 "," f18 "," f19 "," f20 "," f21 "," f22 "," f23 "," f24 "," f25 "," f26 "," f27 "," f28 "," f29 "," rawhide "," unknown_release "," epel "," fedora "," alpha "," arm "," arm64 "," ia64 "," mips "," ppc "," s390 "," sparc "," tilegx "," x86_32 "," x86_64 "," x86_32_e "," x86_32_f "," x86_64_e "," x86_64_f "," ppc_e "," ppc_f "," unknown_arch "," centos "," rhel "," ppc64 "," ppc64le "," modular "," rawhide_modular "," modular_f27 "," modular_f28 "," modular_f29 "," modular_f30;
	};
	olddate=$1
    epel=0;
    fedora=0;
    epel4=0;
    epel5=0;
    epel6=0;
    epel7=0;
    f03=0;
    f04=0;
    f05=0;
    f06=0;
    f07=0;
    f08=0;
    f09=0;
    f10=0;
    f11=0;
    f12=0;
    f13=0;
    f14=0;
    f15=0;
    f16=0;
    f17=0;
    f18=0;
    f19=0;
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
    f30=0;
    rawhide=0;
    rawhide_modular=0;
    modular_f27=0;
    modular_f28=0;
    modular_f29=0;
    modular_f30=0;
    modular=0;
    unknown_release = 0;
    # arch
    alpha=0;
    arm64=0;
    arm=0;
    ia64=0;
    mips=0;
    ppc=0;
    ppc64=0;
    ppc64le=0;
    s390=0;
    sparc=0;
    tilegx=0;
    x86_32=0;
    x86_64=0;
    # sub arch
    ppc_e=0;
    ppc_f=0;
    x86_32_e=0;
    x86_32_f=0;
    x86_64_e = 0;
    x86_64_f = 0;
    unknown_arch = 0;
    centos = 0;
    rhel = 0;
    }

}

END {
  print olddate "," epel4 "," epel5 "," epel6 "," epel7 "," f03 "," f04 "," f05 "," f06 "," f07 "," f08 "," f09 "," f10 "," f11 "," f12 "," f13 "," f14 "," f15 "," f16 "," f17 "," f18 "," f19 "," f20 "," f21 "," f22 "," f23 "," f24 "," f25 "," f26 "," f27 "," f28 "," f29 "," rawhide "," unknown_release "," epel "," fedora "," alpha "," arm "," arm64 "," ia64 "," mips "," ppc "," s390 "," sparc "," tilegx "," x86_32 "," x86_64 "," x86_32_e "," x86_32_f "," x86_64_e "," x86_64_f "," ppc_e "," ppc_f "," unknown_arch "," centos "," rhel "," ppc64 "," ppc64le "," modular "," rawhide_modular "," modular_f27 "," modular_f28 "," modular_f29 "," modular_f30;

}

