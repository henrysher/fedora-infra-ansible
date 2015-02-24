Alias /ui /usr/share/ipsilon/ui
Alias /.well-known /etc/ipsilon/wellknown
WSGIScriptAlias / /usr/sbin/ipsilon
WSGIDaemonProcess ipsilon user=ipsilon group=ipsilon home=/var/lib/ipsilon


<Location />
    WSGIProcessGroup ipsilon
</Location>

<Directory /usr/sbin>
    Require all granted
</Directory>

<Directory /usr/share/ipsilon>
    Require all granted
</Directory>

<Directory /etc/ipsilon/wellknown>
    Require all granted
</Directory>
<Location /.well-known/browserid>
    ForceType application/json
</Location>
