Instructions
------------

The files in this directory are the configuration files for communishift to be applied.

For OIDC auth, get the client secret for "communishift" from ansible-private/files/ipsilon/openidc.production.static, and run:
oc create secret generic fedoraidp-clientsecret --from-literal=clientSecret=<client-secret> -n openshift-config
