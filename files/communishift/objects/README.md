Instructions
------------

The files in this directory are the configuration files for communishift to be applied.

For OIDC auth, get the client secret for "communishift" from ansible-private/files/ipsilon/openidc.production.static, and run:
> oc create secret generic fedoraidp-clientsecret --from-literal=clientSecret=<client-secret> -n openshift-config

For certificates, first install [cert-manager](https://docs.cert-manager.io/en/release-0.10/)
NOTE: The 0.11 version is buggy, as is the operator hub '1.0' version. Use 0.10 unless you want
to spend a lot of time debugging.

Next create the Issuer object. You may need to wait a minute or two for the cert-manager install
to complete and have all pods up.  
To do this, first create a new access key ID and secret key in AWS for the communishift_acme_dns01 user, and update issuer.yml with the access key ID and then create a secret with the private access key
> oc create -f issuer.yml
> oc -n cert-manager create secret generic route53-access-key-secret --from-literal=access-key=THEACCESSKEY
This gives it the ability to create a TXT record for acmechallenges.fedorainfracloud.org.
To allow certificates for other hostnames, those hostnames need a CNAME of "_acme-challenge.<hostname>" pointing to "acmechallenges.fedorainfracloud.org".

After that, create the two certificate requests for the API server and ingress default cert:
> oc -n openshift-config create -f cert_api.yml
> oc -n openshift-ingress create -f cert_apps.yml
This will start the request of the certificates.
Then run the following commands to update the ingress router (will take affect after its restart) and API server with their new certs:

> oc patch apiserver cluster --type=merge -p '{"spec": {"servingCerts": {"namedCertificates": {"names": "api.os.fedorainfracloud.org"}, "servingCertificate": {"name": "api-certificate"}}}}'
> oc patch ingresscontroller.operator default --type=merge -p '{"spec":{"defaultCertificate": {"name": "apps-certificate"}}}' -n openshift-ingress-operator
