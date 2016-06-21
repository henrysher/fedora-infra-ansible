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
        // Don't shorten private pastes.
        if(preg_match('/^http(s)?:\/\/(.+).fedoraproject.org\/(\d+)\/(\d+)\/$/', $long_url)) {
            return $long_url;
        }
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL,"https://da.gd/s?strip");
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array('url' => $long_url)));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
        curl_setopt($ch, CURLOPT_TIMEOUT, 2);
        $result = curl_exec($ch);
        curl_close($ch);
        if (!empty($result))
            return $result;
        else
            return false;

    }
}

?>
