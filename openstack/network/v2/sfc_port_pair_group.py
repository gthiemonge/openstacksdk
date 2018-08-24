# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.network import network_service
from openstack import resource


class SfcPortPairGroup(resource.Resource):
    resource_key = 'port_pair_group'
    resources_key = 'port_pair_groups'
    base_path = '/sfc/port_pair_groups'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'description', 'name', 'port_pairs',
        'port_pair_group_parameters',
        project_id='tenant_id'
    )

    # Properties
    #: The port pair group description.
    description = resource.Body('description')
    #: The port pair group name.
    name = resource.Body('name')
    #: The ID of the project who owns the port pair group. Only administrative
    #: users can specify a project ID other than their own.
    project_id = resource.Body('tenant_id')
    #: The list of port pair IDs or names to apply.
    port_pairs = resource.Body('port_pairs', type=list)
    #: Dictionary of port pair group parameter.
    port_pair_group_parameters = resource.Body('port_pair_group_parameters',
                                               type=dict)
