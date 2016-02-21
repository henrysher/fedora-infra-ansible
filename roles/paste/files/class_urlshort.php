<?php
/**
* Sticky Notes pastebin
* @ver 0.3
* @license BSD License - www.opensource.org/licenses/bsd-license.php
*
* Copyright (c) 2012 Sayak Banerjee <sayakb@kde.org>
* Copyright (c) 2013 Athmane Madjoudj <athmane@fedoraproject.org>
* All rights reserved. Do not remove this copyright notice.
*/

/**
 * URL shortener using ur1.ca from Indenti.ca
 **/
class URLShortener
{
    public function shorten($long_url)
    {
        if(preg_match('/^http(s)?:\/\/(.+).fedoraproject.org\/(\d+)\/(\d+)\/$/', $long_url)) {
            return $long_url;
        }
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL,"http://ur1.ca/");
        curl_setopt($ch, CURLOPT_POST, 1); 
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array('longurl' => $long_url)));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT ,2); 
        curl_setopt($ch, CURLOPT_TIMEOUT, 2);
        $result = curl_exec($ch);
        curl_close($ch);
        preg_match( '/<p class="success">Your ur1 is: <a href="(.+)">(.+)<\/a><\/p>/', $result, $match );
        if (!empty($match)) 
            return $match[1];
        else
            return false;

    }
}

?>
