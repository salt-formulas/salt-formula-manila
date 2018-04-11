# Copyright 2018 Mirantis Inc
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import urllib

from manilang.common import send, MANILA_HEADER


@send('get', MANILA_HEADER)
def list_shares(**kwargs):
    url = '/shares?{}'.format(urllib.urlencode(kwargs))
    return url, None


@send('get', MANILA_HEADER)
def list_shares_detailed(**kwargs):

    url = '/shares/detail?{}'.format(urllib.urlencode(kwargs))
    return url, None


@send('get', MANILA_HEADER)
def get_share_details(share_id, **kwargs):
    url = '/shares/{}'.format(share_id)
    return url, None


@send('post', MANILA_HEADER)
def create_share(share_proto, size, **kwargs):
    url = '/shares'
    json = {
        'share': {
            'share_proto': share_proto,
            'size': size,
        },
    }
    json['share'].update(kwargs)
    return url, json


@send('post', MANILA_HEADER)
def manage_share(protocol, export_path, service_host, **kwargs):
    url = '/shares/manage'
    json = {
        'share': {
            'protocol': protocol,
            'export_path': export_path,
            'service_host': service_host,
        }
    }
    json['share'].update(kwargs)
    return url, json


@send('put', MANILA_HEADER)
def update_share(share_id, **kwargs):
    url = '/shares/{}'.format(share_id)
    json = {
        'share': kwargs,
    }
    return url, json


@send('delete', MANILA_HEADER)
def delete_share(share_id, **kwargs):
    url = '/shares/{}'.format(share_id)
    return url, None
