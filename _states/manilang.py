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

import logging
log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if manila module is present in __salt__
    '''
    return 'manilang' if 'manilang.list_share_types' in __salt__ else False


manilang_func = {
    'list_types': 'manilang.list_share_types',
    'create_type': 'manilang.create_share_type',
    'set_type_specs': 'manilang.set_share_type_extra_specs',
    'unset_type_specs': 'manilang.unset_share_type_extra_specs',
    'delete_type': 'manilang.delete_share_type',
}


def share_type_present(name, extra_specs, cloud_name, **kwargs):
    """
    Ensure that share_type is present and has desired parameters

    This function will create the desired share type if one with the requested
    name does not exist. If it does, it will be updated to correspond to
    parameters passed to this function.

    :param name: name of the share type.
    :param extra_specs: dictionary of extra_specs that share type should have.
    It contains one required parameter - driver_handles_share_servers.
    :param kwargs: other arguments that will be pushed into share_type
        dictionary to be POSTed, if specified.

    """
    origin_share_types = __salt__[
        manilang_func['list_types']
    ](cloud_name=cloud_name)['share_types']
    share_types = [
        share_type
        for share_type in origin_share_types if share_type['name'] == name
    ]
    if not share_types:
        try:
            res = __salt__[
                manilang_func['create_type']
            ](name, extra_specs, cloud_name=cloud_name, **kwargs)
        except Exception as e:
            log.error('Manila share type create failed with {}'.format(e))
            return _create_failed(name, 'resource')
        return _created(name, 'share_type', res)

    elif len(share_types) == 1:
        exact_share_type = share_types[0]

        api_extra_specs = exact_share_type['extra_specs']
        api_keys = set(api_extra_specs)
        sls_keys = set(extra_specs)

        to_delete = api_keys - sls_keys
        to_add = sls_keys - api_keys
        to_update = sls_keys & api_keys
        resp = {}

        for key in to_delete:
            try:
                __salt__[
                    manilang_func['unset_type_specs']
                ](exact_share_type['id'], key, cloud_name=cloud_name)
            except Exception as e:
                log.error(
                    'Manila share type delete '
                    'extra specs failed with {}'.format(e)
                )
                return _update_failed(name, 'share_type_extra_specs')
            resp.update({'deleted_extra_specs': to_delete})

        diff = {}

        for key in to_add:
            diff[key] = extra_specs[key]
        for key in to_update:
            if extra_specs[key] != api_extra_specs[key]:
                diff[key] = extra_specs[key]
        if diff:
            try:
                resp.update(
                    __salt__[
                        manilang_func['set_type_specs']
                    ](exact_share_type['id'], {'extra_specs': diff},
                      cloud_name=cloud_name)
                )
            except Exception as e:
                log.error(
                    'Manila share type update '
                    'extra specs failed with {}'.format(e)
                )
                return _update_failed(name, 'share_type_extra_specs')
        if to_delete or diff:
            return _updated(name, 'share_type', resp)
        return _no_changes(name, 'share_type')
    else:
        return _find_failed(name, 'share_type')


def share_type_absent(name, cloud_name):
    origin_share_types = __salt__[
        manilang_func['list_types']
    ](cloud_name=cloud_name)['share_types']
    share_types = [
        share_type
        for share_type in origin_share_types if share_type['name'] == name
    ]
    if not share_types:
        return _absent(name, 'share_type')
    elif len(share_types) == 1:
        try:
            __salt__[manilang_func['delete_type']](share_types[0]['id'],
                                                   cloud_name=cloud_name)
        except Exception as e:
            log.error('Manila share type delete failed with {}'.format(e))
            return _delete_failed(name, 'share_type')
        return _deleted(name, 'share_type')
    else:
        return _find_failed(name, 'share_type')


def _created(name, resource, resource_definition):
    changes_dict = {
        'name': name,
        'changes': resource_definition,
        'result': True,
        'comment': '{}{} created'.format(resource, name)
    }
    return changes_dict


def _updated(name, resource, resource_definition):
    changes_dict = {
        'name': name,
        'changes': resource_definition,
        'result': True,
        'comment': '{}{} updated'.format(resource, name)
    }
    return changes_dict


def _no_changes(name, resource):
    changes_dict = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '{}{} is in desired state'.format(resource, name)
    }
    return changes_dict


def _deleted(name, resource):
    changes_dict = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '{}{} removed'.format(resource, name)
    }
    return changes_dict


def _absent(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} not present'.format(resource, name),
                    'result': True}
    return changes_dict


def _delete_failed(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} failed to delete'.format(resource,
                                                                 name),
                    'result': False}
    return changes_dict


def _create_failed(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} failed to create'.format(resource,
                                                                 name),
                    'result': False}
    return changes_dict


def _update_failed(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} failed to update'.format(resource,
                                                                 name),
                    'result': False}
    return changes_dict


def _find_failed(name, resource):
    changes_dict = {
        'name': name,
        'changes': {},
        'comment': '{0} {1} found multiple {0}'.format(resource, name),
        'result': False,
    }
    return changes_dict
