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


class SfcPortPair(resource.Resource):
    resource_key = 'port_pair'
    resources_key = 'port_pairs'
    base_path = '/sfc/port_pairs'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'description', 'name', 'ingress', 'egress',
        'service_function_parameters',
        project_id='tenant_id'
    )

    # Properties
    #: The port pair description.
    description = resource.Body('description')
    #: The port pair name.
    name = resource.Body('name')
    #: The ID of the project who owns the port pair. Only administrative
    #: users can specify a project ID other than their own.
    project_id = resource.Body('tenant_id')
    #: The ID of the ingress port.
    ingress = resource.Body('ingress')
    #: The ID of the egress port.
    egress = resource.Body('egress')
    #: Dictionary of service function parameter.
    service_function_parameters = resource.Body('service_function_parameters',
                                                type=dict)
