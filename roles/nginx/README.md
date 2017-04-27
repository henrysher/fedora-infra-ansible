Overview
========

Role for using nginx.  Sets up ssl certs in known locations and inactive
template for application use.


Role options
------------
* `update_ssl_certs` - Only push the SSL key and PEM files and restart Nginx


SSL
---
This role will copy over key/crt by default.
It can be disabled by setting `httpd_no_ssl` to true

You will still need to configure the application to use ssl.  A reference template templates/example_ssl.conf.j2 is provided

The script will look for keys and certs in the paths specified by the
`httpd_ssl_key_file`, `httpd_ssl_crt_file` and `httpd_ssl_pem_file` variables.

If that fails, it will attempt to create key/crt pair if there isn't one already installed.

If a pem file exists in the location specified by `httpd_ssl_pem_file`,
it will be copied across as `ssl.pem`. Applications that required the certificate
chain should point at `/etc/nginx/conf.d/ssl.pem`.

Caveats
-------
The key, crt and pem will always be stored on the host under `/etc/nginx/conf.d/{{
inventory_hostname }}.{key,crt,pem}` due to the multi-sourcing nature of the setup.
Use `httpd_no_ssl` and setup as desired if it deviates from what is covered here.

Logrotate
---------

A default template is configured.

SELinux
-------

selinux contexts are application specific.  Enable the following as needed by your setup:

```
httpd_can_network_relay
httpd_can_network_memcache
httpd_can_network_connect *
httpd_can_network_connect_db *
httpd_can_sendmail
```

- * commonly used items enabled by default

Handlers
--------

restart nginx - restart the nginx service

Variables
---------

* `service_name` - canonical name for service
* `httpd_no_ssl` - don't set up ssl
* `httpd_ssl_key_file` - local path to use as source for ssl.key file
* `httpd_ssl_crt_file` - local path to use as source for ssl.crt file
* `httpd_ssl_pem_file` - local path to use as source for ssl.pem file
* `ssl_fast_dh` - whether to use a speedy method to generate Diffie Hellman
    parameters
* `ssl_intermediate_ca_pattern` - pattern to check if certificate is
    self-signed
* `ssl_self_signed_string` - location and CN settings for self signed cert
