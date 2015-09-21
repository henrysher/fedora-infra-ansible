#!/usr/bin/python
# Copyright 2012  Patrick Uiterwijk <puiterwijk@fedoraproject.org>
# This file has been released as LGPLv3+, see COPYING for the complete license
import sys
import string
import ConfigParser
from argparse import ArgumentParser
from fedora.client import AccountSystem
from oshift_mod import Openshift
from getpass import getpass

def get_keys(host,user,passwd):
    os = Openshift(host=host,user=user,passwd=passwd)
    (resp, content) = os.keys_list()
    if resp != 200:
        print('ERROR! Result: %(resp)s' % {'resp': resp})
        sys.exit(1)
    return os.rest.response.json()['data']

def add_key(host,user,passwd,key_name,key_type,key_contents, verbose=False):
    if verbose:
        print('Adding key %(keyname)s' % {'keyname': key_name})
    os = Openshift(host=host,user=user,passwd=passwd)
    (resp, content) = os.key_add(name=key_name, type=key_type, key_str=key_contents)
    if resp != 200:
        print('ERROR! Result: %(resp)s' % {'resp': resp})
        sys.exit(2)
    if verbose:
        print('Done')
    return os.rest.response.json()['data']

def remove_key(host,user,passwd,key_name, verbose=False):
    if verbose:
        print('Removing key %(keyname)s' % {'keyname': key_name})
    os = Openshift(host=host,user=user,passwd=passwd)
    (resp, content) = os.key_delete(key_name)
    if resp != 200:
        print 'ERROR! Result: %(resp)s' % {'resp': resp}
        sys.exit(3)
    if verbose:
        print('Done')
    return os.rest.response.json()['data']

def get_users_to_have_access(fas, groups):
    all_users = set()
    for group in groups:
        new_users = fas.group_members(group)
        for new_user in new_users:
            all_users.add(new_user['username'])
    return all_users

def get_users_ssh_keys(fas, users):
    keys = {}
    user_data = fas.user_data()
    for userid in user_data.keys():
        if user_data[userid]['username'] in users:
            if user_data[userid]['ssh_key']:
                contents = user_data[userid]['ssh_key']
                if contents.split(' ') > 1:
                    key_type = contents.split(' ')[0]
                    key_contents = contents.split(' ')[1]
                    keys[user_data[userid]['username']] = {'type': key_type, 
                                                       'contents': key_contents,
                                                       'username': user_data[userid]['username']}
    return keys

def get_keys_to_remove(keys_in_openshift, keys_in_fas):
    keys_to_remove = set()
    for key in keys_in_openshift:
        keys_to_remove.add(key['name'])
        for key_in_fas in keys_in_fas:
            if keys_in_fas[key_in_fas]['contents'] == key['content']:
                keys_to_remove.remove(key['name'])
    return keys_to_remove

def get_keys_to_add(keys_in_openshift, keys_in_fas):
    usernames_to_add = set()
    for username in keys_in_fas:
        usernames_to_add.add(username)
        for key in keys_in_openshift:
            if key['content'] == keys_in_fas[username]['contents']:
                usernames_to_add.remove(username)
    keys_to_add = []
    for username in usernames_to_add:
        keys_to_add.append(keys_in_fas[username])
    return keys_to_add

def remove_keys(openshift_host, openshift_user, openshift_pass, to_remove, verbose=False):
    if verbose:
        print('Removing the following keys:')
        print(to_remove)
    for key in to_remove:
        remove_key(openshift_host, openshift_user, openshift_pass, key, verbose=verbose)
    if verbose:
        print('Done')

def add_keys(openshift_host, openshift_user, openshift_pass, to_add, prefix, verbose=False):
    if verbose:
        print('Adding the following keys:')
        print(to_add)
    for key in to_add:
        add_key(openshift_host, openshift_user, openshift_pass, '%(prefix)s%(username)s' % {'prefix': prefix, 'username': key['username']}, key['type'], key['contents'], verbose=verbose)
    if verbose:
        print('Done')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-config_file', help='The configuration file to use', default='/etc/sync-openshift-keys.conf')
    parser.add_argument('--verbose', '-v', help='Make the script more verbose', action='store_true')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config.read(args.config_file)
    fas = AccountSystem(config.get('fas', 'url'), username=config.get('fas', 'user'), password=config.get('fas', 'pass'))
    fas.insecure = True
    if args.verbose:
        print('Getting users...')
    users = get_users_to_have_access(fas, string.split(config.get('general', 'groups'), ','))
    if args.verbose:
        print('Done: %s' % users)
        print('Getting keys in FAS...')
    keys_fas = get_users_ssh_keys(fas, users)
    if args.verbose:
        print('Done: %s')
        print('Getting keys in Openshift...')
    keys_openshift = get_keys(config.get('openshift', 'host'), config.get('openshift', 'user'), config.get('openshift', 'pass'))
    if args.verbose:
        print('Done')
        print('Getting keys to remove...')
    keys_to_remove = get_keys_to_remove(keys_openshift, keys_fas)
    if args.verbose:
        print('Done')
        print('Getting keys to add...')
    keys_to_add = get_keys_to_add(keys_openshift, keys_fas)
    if args.verbose:
        print('Done')
    remove_keys(config.get('openshift', 'host'), config.get('openshift', 'user'), config.get('openshift', 'pass'), keys_to_remove, verbose=args.verbose)
    add_keys(config.get('openshift', 'host'), config.get('openshift', 'user'), config.get('openshift', 'pass'), keys_to_add, config.get('general', 'keyname_prefix'), verbose=args.verbose)
