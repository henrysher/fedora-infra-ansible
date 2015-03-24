#from ansible import errors, runner
#import json
#from novaclient.v3.client import Client
#import novaclient.exceptions;
#
#def flavor_id_to_name(host_vars, user, password, tenant, auth_url):
#    nt = Client(user, password, tenant, auth_url, service_type="compute")
#    try:
#        flavor = nt.flavors.get(host_vars)
#    except novaclient.exceptions.NotFound:
#        raise errors.AnsibleFilterError('There is no flavor of name {0}'.format(host_vars))
#    return flavor.name
#
#
#def flavor_name_to_id(host_vars, user, password, tenant, auth_url):
#    nt = Client(user, password, tenant, auth_url, service_type="compute")
#    for i in nt.flavors.list():
#        if i.name == host_vars:
#          return i.id
#    raise errors.AnsibleFilterError('There is no flavor of id {0}'.format(host_vars))
#
#class FilterModule (object):
#    def filters(self):
#        return {"flavor_id_to_name": flavor_id_to_name,
#            "flavor_name_to_id": flavor_name_to_id,
#        }
