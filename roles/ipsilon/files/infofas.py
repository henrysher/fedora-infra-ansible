# Copyright (C) 2014,2016 Ipsilon project Contributors, for license see COPYING

from ipsilon.info.common import InfoProviderBase, InfoProviderInstaller
from ipsilon.util.plugin import PluginObject
from ipsilon.util.policy import Policy
from ipsilon.util import config as pconfig

from fedora.client.fas2 import AccountSystem


try:
    import openid_cla.cla as cla

    CLA_GROUPS = {
        'cla_click': cla.CLA_URI_FEDORA_CLICK,
        'cla_dell': cla.CLA_URI_FEDORA_DELL,
        'cla_done': cla.CLA_URI_FEDORA_DONE,
        'cla_fedora': cla.CLA_URI_FEDORA_FEDORA,
        'cla_fpca': cla.CLA_URI_FEDORA_FPCA,
        'cla_ibm': cla.CLA_URI_FEDORA_IBM,
        'cla_intel': cla.CLA_URI_FEDORA_INTEL,
        'cla_redhat': cla.CLA_URI_FEDORA_REDHAT,
    }
except ImportError:
    CLA_GROUPS = dict()

fas_mapping = [
    ['username', 'nickname'],
    ['telephone', 'phone'],
    ['country_code', 'country'],
    ['human_name', 'fullname'],
    ['email', 'email'],
    ['timezone', 'timezone'],
    ['ssh_key', 'ssh_key'],
    ['gpg_keyid', 'gpg_keyid'],
]

fas_mapper = Policy(fas_mapping)

aws_idp_arn = 'arn:aws:iam::125523088429:saml-provider/id.fedoraproject.org'
aws_groups = {
    'aws-master': 'arn:aws:iam::125523088429:role/aws-master',
    'aws-iam': 'arn:aws:iam::125523088429:role/aws-iam',
    'aws-billing': 'arn:aws:iam::125523088429:role/aws-billing',
    'aws-atomic': 'arn:aws:iam::125523088429:role/aws-atomic',
    'aws-s3-readonly': 'arn:aws:iam::125523088429:role/aws-s3-readonly',
    'aws-fedoramirror': 'arn:aws:iam::125523088429:role/aws-fedoramirror',
    'aws-s3': 'arn:aws:iam::125523088429:role/aws-s3',
    'aws-cloud-poc': 'arn:aws:iam::125523088429:role/aws-cloud-poc',
}


def fas_make_userdata(fas_data):
    userdata, fas_extra = fas_mapper.map_attributes(fas_data)

    # We need to split ssh keys by newline, since we can't send newlines
    if userdata.get('ssh_key'):
        userdata['ssh_key'] = userdata['ssh_key'].split('\n')

    # compute and store groups and cla groups
    userdata['_groups'] = []
    userdata['_extras'] = {'fas': fas_extra, 'cla': []}
    for group in fas_data.get('approved_memberships', {}):
        if 'name' not in group:
            continue
        if group.get('group_type') == 'cla':
            if group['name'] in CLA_GROUPS:
                group_name = CLA_GROUPS[group['name']]
            else:
                group_name = group['name']
            userdata['_extras']['cla'].append(group_name)
        else:
            userdata['_groups'].append(group['name'])

    userdata['_extras']['awsroles'] = []
    for group in userdata['_groups']:
        if group in aws_groups:
            userdata['_extras']['awsroles'].append(
                '%s,%s' % (aws_idp_arn, aws_groups[group]))

    return userdata


class InfoProvider(InfoProviderBase):

    def __init__(self, *args):
        super(InfoProvider, self).__init__(*args)
        self._fas_client = None
        self.name = 'fas'
        self.description = """
Info plugin that retrieves user data from FAS. """

        self.new_config(
            self.name,
            pconfig.String(
                'FAS url',
                'The FAS Url.',
                'https://admin.fedoraproject.org/accounts/'),
            pconfig.String(
                'FAS Proxy client user Agent',
                'The User Agent presented to the FAS Server.',
                'Ipsilon v1.0'),
            pconfig.Condition(
                'FAS Insecure Auth',
                'If checked skips FAS server cert verification.',
                False),
            pconfig.String(
                'Bind Username',
                'Username to be used when retrieving info.',
                'ipsilondummy'),
            pconfig.String(
                'Bind Password',
                'Username to be used when retrieving info.',
                'Password')
        )

    @property
    def fas_url(self):
        return self.get_config_value('FAS url')

    @property
    def user_agent(self):
        return self.get_config_value('FAS Proxy client user Agent')

    @property
    def insecure(self):
        return self.get_config_value('FAS Insecure Auth')

    @property
    def bind_user(self):
        return self.get_config_value('Bind Username')

    @property
    def bind_pass(self):
        return self.get_config_value('Bind Password')

    @property
    def fas_client(self):
        if not self._fas_client:
            self._fas_client = AccountSystem(base_url=self.fas_url,
                                             insecure=self.insecure,
                                             useragent=self.user_agent,
                                             username=self.bind_user,
                                             password=self.bind_pass)
        return self._fas_client

    def get_user_attrs(self, user):
        if not self.fas_client:
            return {}
        try:
            data = self.fas_client.person_by_username(user)
        except Exception as ex:  # pylint: disable=broad-except
            self.error('Unable to retrieve info for %s: %s' % (user, ex))
            self.debug('URL: %s' % self.fas_url)
            self.debug('username: %s' % self.bind_user)
            return {}
        if not data:
            return {}
        return fas_make_userdata(data)


class Installer(InfoProviderInstaller):

    def __init__(self, *pargs):
        super(Installer, self).__init__()
        self.name = 'fas'
        self.pargs = pargs

    def install_args(self, group):
        group.add_argument('--info-fas', choices=['yes', 'no'], default='no',
                           help='Configure FAS info')
        group.add_argument('--info-fas-bind-username', action='store',
                           help='Username to use to retrieve FAS info')
        group.add_argument('--info-fas-bind-password', action='store',
                           help='Password to use to retrieve FAS info')

    def configure(self, opts, changes):
        if opts['info_fas'] != 'yes':
            return

        # Add configuration data to database
        po = PluginObject(*self.pargs)
        po.name = 'fas'
        po.wipe_data()
        po.wipe_config_values()

        config = dict()
        if 'info_fas_bind_username' in opts:
            config['Bind Username'] = opts['info_fas_bind_username']
        if 'info_fas_bind_password' in opts:
            config['Bind Password'] = opts['info_fas_bind_password']
        po.save_plugin_config(config)

        # Update global config to add login plugin
        po.is_enabled = True
        po.save_enabled_state()
