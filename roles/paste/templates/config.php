<?php
// Sticky Notes Pastebin configuration file
// (C) 2012 Sayak Banerjee. All rights reserved

/// This is an auto generated file
/// Please DO NOT modify manually
/// Unless you are absolutely sure what you're doing ;-)

{% if env == "staging" %}                                             
$db_host = "db02.stg";
{% else %}
$db_host = "db-paste";
{% endif %}

$db_port = "";
$db_name = "pastebin";
$db_username = "{{ pastebin_user }}";
$db_password = "{{ pastebinDBPassword }}";
$db_prefix = "paste_";

$site_name = "Fedora Sticky Notes";
$site_title = "Fedora Project Pastebin";

$site_copyright = "Powered by &lt;a href=&quot;http://www.sayakbanerjee.com/sticky-notes/&quot; rel=&quot;nofollow&quot;&gt;Sticky Notes&lt;/a&gt;. Using &lt;a href=&quot;http://github.com/athmane/sticky-notes-fedora-skin&quot;&gt;Fedora skin&lt;/a&gt;.
&lt;br/&gt;
&quot;Sticky Notes&quot; (the web application) is released under the BSD license,
Copyright &Acirc;&copy; 2012 &lt;a href=&quot;http://sayakbanerjee.com&quot;&gt;Sayak Banerjee&lt;/a&gt;.
&lt;p&gt;&quot;Fedora&quot; and the Fedora logo are trademarks of Red Hat, Inc. The Fedora project is maintained and driven by the community. This is a community maintained site. Red Hat is not responsible for content.&lt;/p&gt;
&lt;p&gt;&lt;a href=&quot;http://fedoraproject.org/en/sponsors&quot;&gt;Sponsors&lt;/a&gt; | &lt;a href=&quot;http://fedoraproject.org/wiki/Legal:Main&quot;&gt;Legal&lt;/a&gt; | &lt;a href=&quot;http://fedoraproject.org/wiki/Legal:Trademark_guidelines&quot;&gt;Trademark Guidelines&lt;/a&gt;&lt;/p&gt;";


$skin_name = "Fedora";
$lang_name = "en-gb";
$admin_skin_name = "Greyscale";
$admin_lang_name = "en-gb";

$sg_services = "ipban,stealth,noflood,php,censor";
$sg_php_key = "";
$sg_php_days = 90;
$sg_php_score = 50;
$sg_php_type = 2;
$sg_censor = "vipshare.me
filevis.com
terafile.co
lafiles.com
salefiles.com
1fichier.com
adf.ly
4shared.com
bayfiles.com
bitshare.com
box.net
ex-load.com
datafile.com
depositfiles.com
esnips.com
file4go.com
filefactory.com
filerio.in
fileom.com
fileserve.com
fileswap.com
freakshare.com
hotfile.com
how-do-i-make-my-computer
jumbofiles.com
keep2share.cc
koofile.com
kookfile.com
lumfile.com
mediafire.com
oteupload.com
putlocker.com
rapidgator.net
rapidshare.com
redload.net
www.secureupload.eu
secureupload.eu
share-online.biz
sharpfile.com
takebin.com
turbobit.net
uppit.com
uploaded.com
uploaded.net
uploading.com
zippyshare.com
zshare.com
3movs.com 
3pic.com 
4tube.com 
89.com 
91porn.com 
adultmovies.com 
adultxpix.net 
amateurs-gone-wild.com 
apetube.com 
askjolene.com 
beeg.com 
bustnow.com 
cliphunter.com 
elephantlist.com 
empflix.com 
glamourbabez.com 
hpornstars.com 
isharemybitch.com 
jerk2it.com 
junocloud.me
keezmovies.com 
linkhumper.com 
maxporn.com 
megaporn.com 
mofosex.com 
nastyrat.com 
officesexx.com 
pichunter.com 
pixandvideo.com 
poguide.com 
pornhub.com
pornolunch.com 
pornrabbit.com 
pornstar-paradise.com 
porntube.com 
pornyeah.com 
redtube.com 
sexmummy.com 
shufuni.com 
slutload.com 
tiava.com 
tjoob.com 
tube8.com 
ultra-pornstars.com 
vho.com 
worldsex.com 
www.kookfile.com
www.uploadable.ch
xhamster.com 
xnxx.com 
xvideos.com 
xxxblackbook.com 
youporn.com 
yourporntube.com 
cl-security.org";

$auth_method = "db";
$ldap_server = "";
$ldap_port = "";
$ldap_base_dn = "";
$ldap_uid = "";
$ldap_filter = "";
$ldap_user_dn = "";
$ldap_password = "";
?>
