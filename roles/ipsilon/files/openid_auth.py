# Copyright (C) 2014 Ipsilon project Contributors, for license see COPYING

from ipsilon.providers.common import ProviderPageBase
from ipsilon.providers.common import AuthenticationError, InvalidRequest
from ipsilon.providers.openid.meta import XRDSHandler, UserXRDSHandler
from ipsilon.providers.openid.meta import IDHandler
from ipsilon.util.policy import Policy
from ipsilon.util.trans import Transaction
from ipsilon.util.user import UserSession

from openid.server.server import ProtocolError, EncodingError

import cherrypy
import time
import json


class AuthenticateRequest(ProviderPageBase):

    def __init__(self, *args, **kwargs):
        super(AuthenticateRequest, self).__init__(*args, **kwargs)
        self.stage = 'init'
        self.trans = None

    def _preop(self, *args, **kwargs):
        try:
            # generate a new id or get current one
            self.trans = Transaction('openid', **kwargs)
            if self.trans.cookie.value != self.trans.provider:
                self.debug('Invalid transaction, %s != %s' % (
                           self.trans.cookie.value, self.trans.provider))
        except Exception, e:  # pylint: disable=broad-except
            raise cherrypy.HTTPRedirect('https://id.stg.fedoraproject.org/')
            self.debug('Transaction initialization failed: %s' % repr(e))
            raise cherrypy.HTTPError(400, 'Invalid transaction id')

    def pre_GET(self, *args, **kwargs):
        self._preop(*args, **kwargs)

    def pre_POST(self, *args, **kwargs):
        self._preop(*args, **kwargs)

    def _get_form(self, *args):
        form = None
        if args is not None:
            first = args[0] if len(args) > 0 else None
            second = first[0] if len(first) > 0 else None
            if isinstance(second, dict):
                form = second.get('form', None)
        return form

    def auth(self, *args, **kwargs):
        request = None
        form = self._get_form(args)
        try:
            request = self._parse_request(**kwargs)
            return self._openid_checks(request, form, **kwargs)
        except InvalidRequest, e:
            raise cherrypy.HTTPError(e.code, e.msg)
        except AuthenticationError, e:
            if request is None:
                raise cherrypy.HTTPError(e.code, e.msg)
            return self._respond(request.answer(False))

    # get attributes, and apply policy mapping and filtering
    def _source_attributes(self, session):
        policy = Policy(self.cfg.default_attribute_mapping,
                        self.cfg.default_allowed_attributes)
        userattrs = session.get_user_attrs()
        mappedattrs, _ = policy.map_attributes(userattrs)
        attributes = policy.filter_attributes(mappedattrs)
        self.debug('Filterd attributes: %s' % repr(attributes))
        return attributes

    def _parse_request(self, **kwargs):
        request = None
        try:
            request = self.cfg.server.decodeRequest(kwargs)
        except ProtocolError, openid_error:
            self.debug('ProtocolError: %s' % openid_error)
            raise InvalidRequest('Invalid OpenID request', 400)

        if request is None:
            self.debug('No request')
            raise cherrypy.HTTPRedirect(self.basepath)

        return request

    def _openid_checks(self, request, form, **kwargs):
        us = UserSession()
        user = us.get_user()
        immediate = False

        self.debug('Mode: %s Stage: %s User: %s' % (
            kwargs['openid.mode'], self.stage, user.name))
        if kwargs.get('openid.mode', None) == 'checkid_setup':
            if user.is_anonymous:
                if self.stage == 'init':
                    returl = '%s/openid/Continue?%s' % (
                        self.basepath, self.trans.get_GET_arg())
                    data = {'openid_stage': 'auth',
                            'openid_request': json.dumps(kwargs),
                            'login_return': returl,
                            'login_target': request.trust_root}
                    self.trans.store(data)
                    redirect = '%s/login?%s' % (self.basepath,
                                                self.trans.get_GET_arg())
                    self.debug('Redirecting: %s' % redirect)
                    raise cherrypy.HTTPRedirect(redirect)
                else:
                    raise AuthenticationError("unknown user", 401)

        elif kwargs.get('openid.mode', None) == 'checkid_immediate':
            # This is immediate, so we need to assert or fail
            if user.is_anonymous:
                return self._respond(request.answer(False))

            immediate = True

        else:
            return self._respond(self.cfg.server.handleRequest(request))

        # check if this is discovery or needs identity matching checks
        if not request.idSelect():
            idurl = self.cfg.identity_url_template % {'username': user.name}
            if request.identity != idurl:
                raise AuthenticationError("User ID mismatch!", 401)

        # check if the relying party is trusted
        if request.trust_root in self.cfg.untrusted_roots:
            raise AuthenticationError("Untrusted Relying party", 401)

        # if the party is explicitly whitelisted just respond
        if request.trust_root in self.cfg.trusted_roots:
            return self._respond(self._response(request, us))

        allowroot = 'allow-%s' % request.trust_root

        try:
            userdata = user.load_plugin_data(self.cfg.name)
            expiry = int(userdata[allowroot])
        except Exception, e:  # pylint: disable=broad-except
            self.debug(e)
            expiry = 0
        if expiry > int(time.time()):
            self.debug("User has unexpired previous authorization")
            return self._respond(self._response(request, us))

        if immediate:
            raise AuthenticationError("No consent for immediate", 401)

        if self.stage == 'consent':
            if form is None:
                raise AuthenticationError("Unintelligible consent", 401)
            allow = form.get('decided_allow', False)
            if not allow:
                raise AuthenticationError("User declined", 401)
            try:
                days = int(form.get('remember_for_days', '0'))
                if days < 0 or days > 7:
                    raise
                userdata = {allowroot: str(int(time.time()) + (days*86400))}
                user.save_plugin_data(self.cfg.name, userdata)
            except Exception, e:  # pylint: disable=broad-except
                self.debug(e)
                days = 0

            # all done we consent!
            return self._respond(self._response(request, us))

        else:
            data = {'openid_stage': 'consent',
                    'openid_request': json.dumps(kwargs)}
            self.trans.store(data)

            # Add extension data to this dictionary
            ad = {
                "Trust Root": request.trust_root,
            }
            userattrs = self._source_attributes(us)
            for n, e in self.cfg.extensions.available().items():
                data = e.get_display_data(request, userattrs)
                self.debug('%s returned %s' % (n, repr(data)))
                for key, value in data.items():
                    ad[self.cfg.mapping.display_name(key)] = value

            context = {
                "title": 'Consent',
                "action": '%s/openid/Consent' % (self.basepath),
                "trustroot": request.trust_root,
                "username": user.name,
                "authz_details": ad,
            }
            context.update(dict((self.trans.get_POST_tuple(),)))
            return self._template('openid/consent_form.html', **context)

    def _response(self, request, session):
        user = session.get_user()
        identity_url = self.cfg.identity_url_template % {'username': user.name}
        response = request.answer(
            True,
            identity=identity_url,
            claimed_id=identity_url
        )
        userattrs = self._source_attributes(session)
        for _, e in self.cfg.extensions.available().items():
            resp = e.get_response(request, userattrs)
            if resp is not None:
                response.addExtension(resp)
        return response

    def _respond(self, response):
        try:
            self.debug('Response: %s' % response)
            do_post_trusts = ['http://taigastg.cloud.fedoraproject.org/', 'http://taiga.cloud.fedoraproject.org/']
            if response.request.trust_root in do_post_trusts:
                webresponse = self.cfg.server.encoder.responseFactory(code=200,
                                                                      body=response.toHTML())
            else:
                webresponse = self.cfg.server.encodeResponse(response)
            cherrypy.response.headers.update(webresponse.headers)
            cherrypy.response.status = webresponse.code
            return webresponse.body
        except EncodingError, encoding_error:
            self.debug('Unable to respond because: %s' % encoding_error)
            cherrypy.response.headers = {
                'Content-Type': 'text/plain; charset=UTF-8'
            }
            cherrypy.response.status = 400
            return encoding_error.response.encodeToKVForm()


class Continue(AuthenticateRequest):

    def GET(self, *args, **kwargs):
        transdata = self.trans.retrieve()
        self.stage = transdata.get('openid_stage', None)
        openid_request = transdata.get('openid_request', None)
        if self.stage is None or openid_request is None:
            raise AuthenticationError("unknown state", 400)

        kwargs = json.loads(openid_request)
        return self.auth(**kwargs)


class Consent(AuthenticateRequest):

    def POST(self, *args, **kwargs):
        transdata = self.trans.retrieve()
        self.stage = transdata.get('openid_stage', None)
        openid_request = transdata.get('openid_request', None)
        if self.stage is None or openid_request is None:
            raise AuthenticationError("unknown state", 400)

        args = ({'form': kwargs},)
        kwargs = json.loads(openid_request)
        return self.auth(*args, **kwargs)


class OpenID(AuthenticateRequest):

    def __init__(self, *args, **kwargs):
        super(OpenID, self).__init__(*args, **kwargs)
        self.XRDS = XRDSHandler(*args, **kwargs)
        self.yadis = UserXRDSHandler(*args, **kwargs)
        self.id = IDHandler(*args, **kwargs)
        self.Continue = Continue(*args, **kwargs)
        self.Consent = Consent(*args, **kwargs)
        self.trans = None

    def GET(self, *args, **kwargs):
        return self.auth(**kwargs)

    def POST(self, *args, **kwargs):
        return self.auth(**kwargs)
