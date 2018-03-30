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

from manilang.common import send, MANILA_HEADER


@send('get', MANILA_HEADER)
def list_share_types(**kwargs):
    url = '/types'
    return url, None


@send('get', MANILA_HEADER)
def get_default_share_types(**kwargs):
    url = '/types/default'
    return url, None


@send('get', MANILA_HEADER)
def get_share_type_detail(share_type_id, **kwargs):
    url = '/types/{}'.format(share_type_id)
    return url, None


@send('get', MANILA_HEADER)
def get_extra_specs(share_type_id, **kwargs):
    url = '/types/{}/extra_specs'.format(share_type_id)
    return url, None


@send('post', MANILA_HEADER)
def create_share_type(name, extra_specs, **kwargs):
    json = {
        'share_type': {
            'extra_specs': extra_specs,
            'name': name,
        }
    }
    # NOTE: passing share_type dictionary in kwargs will override anything
    #       that was constructed from function arguments. Use with caution.
    #       is_public attribute is special, as os-share-type-access:is_public
    #       always overrides share_type_access:is_public, no matter what
    #       microversion used (sic!).
    json['share_type'].update(kwargs)
    url = '/types'
    return url, json


@send('get', MANILA_HEADER)
def get_share_type_access_details(share_type_id, **kwargs):
    url = '/types/{}/share_type_access'.format(share_type_id)
    return url, None


@send('post', MANILA_HEADER)
def set_share_type_extra_specs(share_type_id, extra_specs, **kwargs):
    url = '/types/{}/extra_specs'.format(share_type_id)
    json = {
        'extra_specs': extra_specs
    }
    return url, json


@send('delete', MANILA_HEADER)
def unset_share_type_extra_specs(share_type_id, extra_spec_key, **kwargs):
    url = '/types/{}/extra_specs/{}'.format(share_type_id, extra_spec_key)
    return url, None


@send('post', MANILA_HEADER)
def add_share_type_access(share_type_id, project, **kwargs):
    url = '/types/{}/action'.format(share_type_id)
    json = {
        'addProjectAccess': {
            'project': project
        }
    }
    return url, json


@send('post', MANILA_HEADER)
def remove_share_type_access(share_type_id, project, **kwargs):
    url = 'types/{}/action'.format(share_type_id)
    json = {
        'removeProjectAccess': {
            'project': project
        }
    }
    return url, json


@send('delete', MANILA_HEADER)
def delete_share_type(share_type_id, **kwargs):
    url = '/types/{}'.format(share_type_id)
    return url, None
