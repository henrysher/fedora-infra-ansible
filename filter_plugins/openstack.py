from ansible import errors, runner
from glanceclient  import Client as GlanceClient
from keystoneclient import session
from keystoneclient.auth.identity import v2 as identity
from novaclient.v3.client import Client
import glanceclient.exc
import json
import novaclient.exceptions

def flavor_id_to_name(host_vars, user, password, tenant, auth_url):
    nt = Client(user, password, tenant, auth_url, service_type="compute")
    try:
        flavor = nt.flavors.get(host_vars)
    except novaclient.exceptions.NotFound:
        raise errors.AnsibleFilterError('There is no flavor of name {0}'.format(host_vars))
    return flavor.name


def flavor_name_to_id(host_vars, user, password, tenant, auth_url):
    nt = Client(user, password, tenant, auth_url, service_type="compute")
    for i in nt.flavors.list():
        if i.name == host_vars:
          return i.id
    raise errors.AnsibleFilterError('There is no flavor of id {0}'.format(host_vars))

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
        raise errors.AnsibleFilterError('There is no image of id {0}'.format(host_vars))

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
    raise errors.AnsibleFilterError('There is no image of name {0}'.format(host_vars))

class FilterModule (object):
    def filters(self):
        return {"flavor_id_to_name": flavor_id_to_name,
            "flavor_name_to_id": flavor_name_to_id,
            "image_id_to_name": image_id_to_name,
            "image_name_to_id": image_name_to_id,
        }
