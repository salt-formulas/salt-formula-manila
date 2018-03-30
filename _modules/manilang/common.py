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

import os_client_config


MANILA_HEADER = 'X-OpenStack-Manila-API-Version'


log = logging.getLogger(__name__)


class ManilaException(Exception):

    _msg = "Manila module exception occured."

    def __init__(self, message=None, **kwargs):
        super(ManilaException, self).__init__(message or self._msg)


class NoManilaEndpoint(ManilaException):
    _msg = "Manila endpoint not found in keystone catalog."


class NoAuthPluginConfigured(ManilaException):
    _msg = ("You are using keystoneauth auth plugin that does not support "
            "fetching endpoint list from token (noauth or admin_token).")


class NoCredentials(ManilaException):
    _msg = "Please provide cloud name present in clouds.yaml."


def _get_raw_client(cloud_name):
    service_type = 'sharev2'
    adapter = os_client_config.make_rest_client(service_type,
                                                cloud=cloud_name)
    try:
        access_info = adapter.session.auth.get_access(adapter.session)
        endpoints = access_info.service_catalog.get_endpoints()
    except (AttributeError, ValueError):
        e = NoAuthPluginConfigured()
        log.error('%s' % e)
        raise e
    if service_type not in endpoints:
        service_type = None
        for possible_type in ('share', 'shared-file-system'):
            if possible_type in endpoints:
                service_type = possible_type
                break
        if not service_type:
            e = NoManilaEndpoint()
            log.exception('%s' % e)
            raise e
        adapter = os_client_config.make_rest_client(service_type,
                                                    cloud=cloud_name)
    log.debug("Using manila endpoint with type %s." % service_type)
    return adapter


def send(method, microversion_header=None):
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            headers = kwargs.pop('headers', {})
            if kwargs.get('microversion'):
                headers.setdefault(microversion_header,
                                   kwargs.get('microversion'))
            cloud_name = kwargs.pop('cloud_name')
            if not cloud_name:
                e = NoCredentials()
                log.error('%s' % e)
                raise e
            adapter = _get_raw_client(cloud_name)
            url, json = func(*args, **kwargs)
            if json:
                response = getattr(adapter, method)(url, headers=headers,
                                                    json=json)
            else:
                response = getattr(adapter, method)(url, headers=headers)
            if not response.content:
                return {}
            return response.json()
        return wrapped_f
    return wrap
