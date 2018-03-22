import logging


try:
    import os_client_config
    from keystoneauth1 import exceptions as ka_exceptions
    REQUIREMENTS_MET = True
except ImportError:
    REQUIREMENTS_MET = False


def __virtual__():
    """Only load manilang if requirements are available."""
    if REQUIREMENTS_MET:
        return 'manilang'
    else:
        return False, ("The manilang execution module cannot be loaded: "
                       "os_client_config or keystoneauth are unavailable.")


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
            log.error('%s' % e)
            raise e
        adapter = os_client_config.make_rest_client(service_type,
                                                    cloud=cloud_name)
    log.debug("Using manila endpoint with type %s." % service_type)
    return adapter


def _add_microversion_header(microversion, headers):
    if microversion:
        headers.setdefault('X-OpenStack-Manila-API-Version', microversion)


def create_adapter(fun):
    def inner(*args, **kwargs):
        headers = kwargs.pop('headers', {})
        _add_microversion_header(kwargs.get('microversion'), headers)
        cloud_name = kwargs.get('cloud_name')
        if not cloud_name:
            e = NoCredentials()
            log.error('%s' % e)
            raise e
        adapter = _get_raw_client(cloud_name)
        return fun(*args, adapter=adapter, headers=headers, **kwargs)
    return inner


@create_adapter
def get_default_share_types(**kwargs):
    adapter = kwargs.get('adapter')
    try:
        response = adapter.get('/types/default',
                               headers=kwargs.get('headers', {}))
    except ka_exceptions.NotFound:
        log.debug("No default share type found.")
        return None
    return response.json()


@create_adapter
def create_share_type(name, driver_handles_share_servers, extra_specs=None,
                      is_public=True, **kwargs):
    adapter = kwargs.get('adapter')
    extra_specs = extra_specs or {}
    extra_specs['driver_handles_share_servers'] = driver_handles_share_servers
    post_data = {
        'share_type': {
            'extra_specs': extra_specs, 'name': name,
            'os-share-type-access:is_public': is_public}}
    # NOTE: passing share_type dictionary in kwargs will override anything
    #       that was constructed from function arguments. Use with caution.
    #       is_public attribute is special, as os-share-type-access:is_public
    #       always overrides share_type_access:is_public, no matter what
    #       microversion used (sic!).
    post_data['share_type'].update(kwargs.get('share_type', {}))
    response = adapter.post('/types', json=post_data,
                            headers=kwargs.get('headers', {}))
    return response.json()['share_type']
