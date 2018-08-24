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


class SfcPortChain(resource.Resource):
    resource_key = 'port_chain'
    resources_key = 'port_chains'
    base_path = '/sfc/port_chains'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'description', 'name', 'port_pair_groups',
        'flow_classifiers', 'chain_parameters', 'chain_id',
        project_id='tenant_id'
    )

    # Properties
    #: The port chain description.
    description = resource.Body('description')
    #: The port chain name.
    name = resource.Body('name')
    #: The ID of the project who owns the port chain. Only administrative
    #: users can specify a project ID other than their own.
    project_id = resource.Body('tenant_id')
    #: The list of port pair group IDs or names to apply.
    port_pair_groups = resource.Body('port_pair_groups', type=list)
    #: The list of flow classifier IDs or names to apply.
    flow_classifiers = resource.Body('flow_classifiers', type=list)
    #: Dictionary of port chain parameters.
    chain_parameters = resource.Body('chain_parameters', type=dict)
    #: The ID of the port chain.
    chain_id = resource.Body('chain_id', type=int)
