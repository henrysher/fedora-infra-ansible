#
# Take the apache log line
# 123.115.133.104 - - [01/Jan/2015:04:02:01 +0000] "GET /zh_CN/server/download/server-download-splash?file=http://download.fedoraproject.org/pub/fedora/linux/releases/21/Server/i386/iso/Fedora-Server-DVD-i386-21.iso HTTP/1.1" 200 4355 "https://getfedora.org/zh_CN/server/download/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
# Convert to
# 2012-10-30:13:5 123.115.133.104 Fedora-Server-DVD-i386-21.iso

function convertdate(str) {
  gsub(/\[/, "", str)
  split(str,a,":");
  split(a[1],b,"/");
  temp="";
  switch (b[2]) {
  case "Jan":
    temp="01"
    break;
  case "Feb":
    temp="02"
    break;
  case "Mar":
    temp="03"
    break;
  case "Apr":
    temp="04"
    break;
  case "May":
    temp="05"
    break;
  case "Jun":
    temp="06"
    break;
  case "Jul":
    temp="07"
    break;
  case "Aug":
    temp="08"
    break;
  case "Sep":
    temp="09"
    break;
  case "Oct":
    temp="10"
    break;
  case "Nov":
    temp="11"
    break;
  case "Dec":
    temp="12"
    break;
  default:
    temp="00"
    break;
  }
  foo=substr(a[3],1,1);
  return b[3]"-"temp"-"b[1]
}

function getimage(str) {
  if (str ~/=/) {
    split(str,a,"=");
    x=split(a[2],b,"/");
    return b[x]
  } else {
    x=split(str,b,"/");
    return b[x]
  }
}

$7 ~/\.qcow2$|\.iso$|\.raw\.xz$|\.box$/ && $6 ~/GET/ && $9 ~/302|200/ {
  date = convertdate($4)
  iso = getimage($7)
  ip = $1
  print date, ip, iso
}

