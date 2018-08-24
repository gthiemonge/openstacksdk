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


class SfcFlowClassifier(resource.Resource):
    resource_key = 'flow_classifier'
    resources_key = 'flow_classifiers'
    base_path = '/sfc/flow_classifiers'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'description', 'name', 'ethertype', 'protocol',
        'source_port_range_min', 'source_port_range_max',
        'destination_port_range_min', 'destination_port_range_max',
        'source_ip_prefix', 'destination_ip_prefix',
        'logical_source_port', 'logical_destination_port',
        'l7_parameters',
        project_id='tenant_id',
    )

    # Properties
    #: The flow classifier description.
    description = resource.Body('description')
    #: The flow classifier name.
    name = resource.Body('name')
    #: The ID of the project who owns the flow classifier. Only administrative
    #: users can specify a project ID other than their own.
    project_id = resource.Body('tenant_id')
    #: L2 ethertype. Defaults to "IPv4".
    ethertype = resource.Body('ethertype')
    #: L3 protocol.
    protocol = resource.Body('protocol')
    #: Source protocol port Minimum.
    source_port_range_min = resource.Body('source_port_range_min', type=int)
    #: Source protocol port Maximum.
    source_port_range_max = resource.Body('source_port_range_max', type=int)
    #: Destination protocol port Minimum.
    destination_port_range_min = resource.Body('destination_port_range_min',
                                               type=int)
    #: Destination protocol port Maximum.
    destination_port_range_max = resource.Body('destination_port_range_max',
                                               type=int)
    #: Source ip prefix.
    source_ip_prefix = resource.Body('source_ip_prefix')
    #: Destination ip prefix.
    destination_ip_prefix = resource.Body('destination_ip_prefix')
    #: ID or name of the neutron source port.
    logical_source_port = resource.Body('logical_source_port')
    #: ID or name of the neutron destination port.
    logical_destination_port = resource.Body('logical_destination_port')
    #: L7 parameters.
    l7_parameters = resource.Body('l7_parameters')
