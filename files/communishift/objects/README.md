Instructions
------------

The files in this directory are the configuration files for communishift to be applied.

For OIDC auth, get the client secret for "communishift" from ansible-private/files/ipsilon/openidc.production.static, and run:
> oc create secret generic fedoraidp-clientsecret --from-literal=clientSecret=<client-secret> -n openshift-config

For certificates, first install [cert-manager](https://docs.cert-manager.io/en/latest/), and then create the Issuer object.
To do this, first create a new access key ID and secret key in AWS for the communishift_acme_dns01 user, and update issuer and create a secret:
> oc create secret generic route53-access-key-secret --from-literal=access-key=THEACCESSKEY
This gives it the ability to create a TXT record for acmechallenges.fedorainfracloud.org.
To allow certificates for other hostnames, those hostnames need a CNAME of "_acme-challenge.<hostname>" pointing to "acmechallenges.fedorainfracloud.org".
After that, create the two certificate requests for the API server and ingress default cert:
> oc -n openshift-config create -f cert_api.yml
> oc -n openshift-ingress create -f cert_apps.yml
This will start the request of the certificates.
Then run the following commands to update the ingress router (will take affect after its restart) and API server with their new certs:
> oc patch apiserver cluster --type=merge -p '{"spec": {"servingCerts": {"defaultServingCertificate": {"name": "api-certificate"}}}}'
> oc patch ingresscontroller.operator default --type=merge -p '{"spec":{"defaultCertificate": {"name": "apps-certificate"}}}' -n openshift-ingress-operator
