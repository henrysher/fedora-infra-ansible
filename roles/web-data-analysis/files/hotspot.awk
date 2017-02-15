#
# Take the apache log line
# 83.163.161.147 - - [30/Sep/2012:13:54:19 +0000] "GET /static/hotspot.txt HTTP/1.1" 200 3 "-" "dnssec-trigger/0.11"
# Convert to
# 1349013000 1

function convertdate(str) {
  gsub(/\[/, "", str)
  gsub(/\]/, "", str)
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
  x=b[3]" "temp" "b[1]" "a[2]" "a[3] " "a[4]
  y=int(mktime(x)/300) # 300 seconds make 5 minutes (I NEED A GLOBAL VAR)
  return y
}


BEGIN{
  timestamp=0;
  num_ts = 0;
  ts_hotspots=0;
  total_hotsponts=0;
}

#
# We assume that every 300 seconds a system will log in at least 1
# time because the Networkmanager addon does so.
# Convert our date stamp to the nearest 5 minute block and add data to
# it. If the log file goes backwards or jumps etc this will mean
# multiple outputs for a timestamp. A later process will need to deal
# with that. All this will do is output how many it saw at that block
# in the log file.
#

$7 ~/hotspot.txt/ && $6 ~/GET/ {
  date = convertdate($4)
  if (timestamp != date) {
    num_ts = num_ts +1;
    print (timestamp*300),ts_hotspots # GLOBAL VAR GOES HERE
    timestamp = date;
    ts_hotspots = 1;
  } else {
    ts_hotspots = ts_hotspots +1;
    total_hotspots = total_hotspots +1;
  }
}

END {
  num_ts = num_ts +1;
  print int(timestamp*300),ts_hotspots # LOOK GLOBAL VAR AGAIN                                                                                                             
}

## END OF FILE
