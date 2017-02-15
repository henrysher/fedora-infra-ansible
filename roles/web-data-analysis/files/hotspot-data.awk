BEGIN{
  date=strftime("%F",0);
  count=1;
  sum=0;
  most=0;
  least=0
  print date ",AVG,LEAST,MAX"
}

{
  newdate=strftime("%F",$1);                # convert this to a printable date
  if (date != newdate){
    print date "," int(sum/count) "," least "," most;
    date=newdate;
    count=1;    # start count to 0. we should have 288 per day but logs are stupid
    sum=$2;     # start the sum
    most=$2;    # what is going to be our most per day
    least=$2;   # what is going to be our least per day
  } else {
    count=count+1;
    sum=sum+$2;
    if ($2 > most){
      most=$2;
    };
    if ($2 < least) {
      least=$2;
    }
  }
}

END{
  print date "," int(sum/count) "," least "," most;
}
