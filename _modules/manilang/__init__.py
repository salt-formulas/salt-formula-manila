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

try:
    import os_client_config
    from keystoneauth1 import exceptions as ka_exceptions
    REQUIREMENTS_MET = True
except ImportError:
    REQUIREMENTS_MET = False

from manilang import share_types

list_share_types = share_types.list_share_types
create_share_type = share_types.create_share_type
set_share_type_extra_specs = share_types.set_share_type_extra_specs
unset_share_type_extra_specs = share_types.unset_share_type_extra_specs
delete_share_type = share_types.delete_share_type


__all__ = (
    'list_share_types', 'create_share_type',
    'set_share_type_extra_specs', 'unset_share_type_extra_specs',
    'delete_share_type',
)


def __virtual__():
    """Only load manilang if requirements are available."""
    if REQUIREMENTS_MET:
        return 'manilang'
    else:
        return False, ("The manilang execution module cannot be loaded: "
                       "os_client_config or keystoneauth are unavailable.")
