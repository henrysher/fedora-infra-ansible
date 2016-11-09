#!/bin/bash
#renew letsencrypt certificate. it checks if cert need renewal. if not nginx will not stop
# check and renew if required, quietly. if so do it in standalone mode
/usr/bin/certbot renew -q --pre-hook "/usr/bin/systemctl stop nginx" --post-hook "/usr/bin/systemctl start nginx"

