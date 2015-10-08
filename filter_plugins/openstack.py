from ansible import errors
from glanceclient  import Client as GlanceClient
from keystoneclient import session
from keystoneclient.auth.identity import v2 as identity
from neutronclient.neutron.client import Client as NeutronClient
from novaclient.v3.client import Client
import glanceclient.exc
import json
import novaclient.exceptions

def flavor_id_to_name(host_vars, user, password, tenant, auth_url):
    nt = Client(user, password, tenant, auth_url, service_type="compute")
    try:
        flavor = nt.flavors.get(host_vars)
    except novaclient.exceptions.NotFound:
        raise errors.AnsibleFilterError('There is no flavor of name {0} accessible for tenant {1}'.format(host_vars, tenant))
    return flavor.name


def flavor_name_to_id(host_vars, user, password, tenant, auth_url):
    nt = Client(user, password, tenant, auth_url, service_type="compute")
    for i in nt.flavors.list():
        if i.name == host_vars:
          return i.id
    raise errors.AnsibleFilterError('There is no flavor of id {0} accessible for tenant {1}'.format(host_vars, tenant))

def image_id_to_name(host_vars, user, password, tenant, auth_url):
    auth = identity.Password(auth_url=auth_url, username=user,
                         password=password, tenant_name=tenant)
    sess = session.Session(auth=auth)
    token = auth.get_token(sess)
    endpoint = auth.get_endpoint(sess, service_name='glance', service_type='image')
    glance = GlanceClient('2', endpoint=endpoint, token=token)
    try:
          return glance.images.get(host_vars).name
    except glanceclient.exc.HTTPNotFound:
        raise errors.AnsibleFilterError('There is no image of id {0} accessible for tenant {1}'.format(host_vars, tenant))

def image_name_to_id(host_vars, user, password, tenant, auth_url):
    auth = identity.Password(auth_url=auth_url, username=user,
                         password=password, tenant_name=tenant)
    sess = session.Session(auth=auth)
    token = auth.get_token(sess)
    endpoint = auth.get_endpoint(sess, service_name='glance', service_type='image')
    glance = GlanceClient('2', endpoint=endpoint, token=token)
    for i in glance.images.list():
        if i.name == host_vars:
          return i.id
    raise errors.AnsibleFilterError('There is no image of name {0} accessible for tenant {1}'.format(host_vars, tenant))

def network_name_to_id(host_vars, user, password, tenant, auth_url):
    """ Accept one name of network or list of names of networks and return the same
    structure, but names replaced by ids of the network(s). """
    auth = identity.Password(auth_url=auth_url, username=user,
                         password=password, tenant_name=tenant)
    sess = session.Session(auth=auth)
    token = auth.get_token(sess)
    endpoint = auth.get_endpoint(sess, service_name='neutron', service_type='network')
    neutron = NeutronClient('2.0', endpoint_url=endpoint, token=token)
    result_as_list = isinstance(host_vars, list)
    if not result_as_list:
        host_vars = [host_vars]
    result = []
    for net in host_vars:
        networks = neutron.list_networks(name=net, fields='name')["networks"]
        if networks:
            result += [networks[0]['id']]
        else:
            raise errors.AnsibleFilterError('There is no network of name {0} accessible for tenant {1}'.format(net, tenant))
    if result_as_list:
        return result
    else:
        return result[0]

def network_id_to_name(host_vars, user, password, tenant, auth_url):
    """ Accept one id of network or list of ids of networks and return the same
    structure, but ids replaced by name of the network(s). """
    auth = identity.Password(auth_url=auth_url, username=user,
                         password=password, tenant_name=tenant)
    sess = session.Session(auth=auth)
    token = auth.get_token(sess)
    endpoint = auth.get_endpoint(sess, service_name='neutron', service_type='network')
    neutron = NeutronClient('2.0', endpoint_url=endpoint, token=token)
    result_as_list = isinstance(host_vars, list)
    if not result_as_list:
        host_vars = [host_vars]
    result = []
    for net in host_vars:
        networks = neutron.list_networks(id=net, fields='name')["networks"]
        if networks:
            result += [networks[0]['name']]
        else:
            raise errors.AnsibleFilterError('There is no network of id {0} accessible for tenant {1}'.format(net, tenant))
    if result_as_list:
        return result
    else:
        return result[0]

class FilterModule (object):
    def filters(self):
        return {"flavor_id_to_name": flavor_id_to_name,
            "flavor_name_to_id": flavor_name_to_id,
            "image_id_to_name": image_id_to_name,
            "image_name_to_id": image_name_to_id,
            "network_name_to_id": network_name_to_id,
            "network_id_to_name": network_id_to_name,
        }
