# Copyright (C) 2015 Patrick Uiterwijk, for license see COPYING

from __future__ import absolute_import

try:
    from ipsilon.info.infofas import fas_make_userdata
except ImportError:
    fas_make_userdata = None
from ipsilon.providers.openid.extensions.common import OpenidExtensionBase
import ipsilon.root
from ipsilon.util.page import Page
from ipsilon.util.user import User

import json
import inspect


class OpenidExtension(OpenidExtensionBase):

    def __init__(self, *pargs):
        super(OpenidExtension, self).__init__('API')

    def enable(self):
        # This is the most ugly hack in my history of python...
        # But I need to find the root object, and that is not passed into
        #  the OpenID extension system anywhere...
        root_obj = inspect.stack()[5][0].f_locals['self']
        root_obj.api = APIPage(root_obj)


class APIPage(Page):
    def __init__(self, root_obj):
        ipsilon.root.sites['api'] = dict()
        ipsilon.root.sites['api']['template_env'] = \
            ipsilon.root.sites['default']['template_env']
        super(APIPage, self).__init__(ipsilon.root.sites['api'])
        self.v1 = APIV1Page(root_obj)


class APIV1Page(Page):
    def __init__(self, root_obj):
        ipsilon.root.sites['api_v1'] = dict()
        ipsilon.root.sites['api_v1']['template_env'] = \
            ipsilon.root.sites['default']['template_env']
        super(APIV1Page, self).__init__(ipsilon.root.sites['api_v1'])
        self.root_obj = root_obj

    def root(self, *args, **kwargs):
        return json.dumps(self._perform_call(kwargs))

    def _perform_call(self, arguments):
        required_arguments = ['auth_module', 'username', 'password']
        for arg in required_arguments:
            if not arg in arguments:
                return {'success': False,
                        'status': 400,
                        'message': 'Missing argument: %s' % arg
                        }

        fas = self.root_obj.login.fas.lm
        openid = self.root_obj.openid

        openid_request = None
        try:
            openid_request = openid.cfg.server.decodeRequest(arguments)
        except Exception, ex:
            print 'Error during openid decoding: %s' % ex
            return {'success': False,
                    'status': 400,
                    'message': 'Invalid request'
                    }
        if not openid_request:
            print 'No OpenID request parsed'
            return {'success': False,
                    'status': 400,
                    'message': 'Invalid request'
                    }
        if not arguments['auth_module'] == 'fedoauth.auth.fas.Auth_FAS':
            print 'Unknown auth module selected'
            return {'success': False,
                    'status': 400,
                    'message': 'Unknown authentication module'
                    }
        username = arguments['username']
        password = arguments['password']
        user = None
        userdata = None
        try:
            _, user = fas.fpc.login(username, password)
            if fas_make_userdata is None:
                userdata = fas.page.make_userdata(user.user)
            else:
                userdata = fas_make_userdata(user.user)
        except Exception, ex:
            print 'Error during auth: %s' % ex
            pass

        if user is None or userdata is None:
            print 'No user or data: %s, %s' % (user, userdata)
            return {'success': False,
                    'status': 400,
                    'message': 'Authentication failed'}

        us_obj = User(username)
        fake_session = lambda: None
        setattr(fake_session, 'get_user', lambda *args: us_obj)
        setattr(fake_session, 'get_user_attrs', lambda *args: userdata)

        openid_response = openid._response(openid_request, fake_session)
        openid_response = openid.cfg.server.signatory.sign(openid_response).fields.toPostArgs()
        return {'success': True,
                'response': openid_response}

