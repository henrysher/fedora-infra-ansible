<?php
$region = $_POST['region'];
$realname = $_POST['realname'];
$email = $_POST['email'];
$media = $_POST['media'];
#$address = str_replace("\r\n", "[[BR]]", $_POST['address']);//To replace all the new lines with wiki formatting
#$address1 = $_POST['address1'];
#$address2 = $_POST['address2'];
#$address3 = $_POST['address3'];
#$country = $_POST['address4'];

$special_characters = array('#','!',"@","/","'","\"");
$address1 = str_replace($special_characters, "", $_POST['address1']);
$address2 = str_replace($special_characters, "", $_POST['address2']);
$address3 = str_replace($special_characters, "", $_POST['address3']);
$country = str_replace($special_characters, "", $_POST['address4']);
$country = strtoupper($country);


$keywords = date("F Y");
$release = $_POST['release'];

if (empty($realname) || empty($email) || empty($address1) || empty($address2) || empty($address3) || empty($country)){
   header( "Location: FreeMedia-error.html");
exit;
}

//removing this per Neville's reques, this page currently is a dead end
#if ($country == "BRAZIL"){header("Location: http://www.projetofedora.org/guf_grupos_usuarios_fedora");
#exit;
#}


if ($country == "IRAN" || $country == "CUBA" || $country == "IRAQ" || $country == "KOREA, DEMOCRATIC PEOPLES REPUBLIC OF" || $country == "SUDAN"||$country == "SYRIAN ARAB REPUBLIC"){header( "Location: FreeMedia-error-embargoed-destination.html");
exit;
}

header("Location: https://fedorahosted.org/freemedia/newticket?reporter=$email&summary= $realname from $country wants a $media.&description=$realname,[[BR]]$address1 [[BR]]$address2 [[BR]]$address3 [[BR]]$country.[[BR]] &version=$media&keywords=$region, $release, $keywords&email=$email&country=$country");
exit;
?>
