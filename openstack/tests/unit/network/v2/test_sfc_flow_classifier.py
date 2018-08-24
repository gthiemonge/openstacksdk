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

import testtools

from openstack.network.v2 import sfc_flow_classifier

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'description': '1',
    'name': '2',
    'tenant_id': '3',
    'ethertype': '4',
    'protocol': '5',
    'source_port_range_min': 6,
    'source_port_range_max': 7,
    'destination_port_range_min': 8,
    'destination_port_range_max': 9,
    'source_ip_prefix': '10',
    'destination_ip_prefix': '11',
    'logical_source_port': '12',
    'logical_destination_port': '12',
    'l7_parameters': {'13': '13'},
}


class TestSfcFlowClassifier(testtools.TestCase):

    def test_basic(self):
        sot = sfc_flow_classifier.SfcFlowClassifier()
        self.assertEqual('flow_classifier', sot.resource_key)
        self.assertEqual('flow_classifiers', sot.resources_key)
        self.assertEqual('/sfc/flow_classifiers', sot.base_path)
        self.assertEqual('network', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({"description": "description",
                              "name": "name",
                              "project_id": "tenant_id",
                              "ethertype": "ethertype",
                              "protocol": "protocol",
                              "source_port_range_min":
                                  "source_port_range_min",
                              "source_port_range_max":
                                  "source_port_range_max",
                              "destination_port_range_min":
                                  "destination_port_range_min",
                              "destination_port_range_max":
                                  "destination_port_range_max",
                              "source_ip_prefix": "source_ip_prefix",
                              "destination_ip_prefix":
                                  "destination_ip_prefix",
                              "logical_source_port": "logical_source_port",
                              "logical_destination_port":
                                  "logical_destination_port",
                              "l7_parameters": "l7_parameters",
                              "limit": "limit",
                              "marker": "marker"},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = sfc_flow_classifier.SfcFlowClassifier(**EXAMPLE)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)

        self.assertEqual(EXAMPLE['ethertype'], sot.ethertype)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
        self.assertEqual(EXAMPLE['source_port_range_min'],
                         sot.source_port_range_min)
        self.assertEqual(EXAMPLE['source_port_range_max'],
                         sot.source_port_range_max)
        self.assertEqual(EXAMPLE['destination_port_range_min'],
                         sot.destination_port_range_min)
        self.assertEqual(EXAMPLE['destination_port_range_max'],
                         sot.destination_port_range_max)
        self.assertEqual(EXAMPLE['source_ip_prefix'], sot.source_ip_prefix)
        self.assertEqual(EXAMPLE['destination_ip_prefix'],
                         sot.destination_ip_prefix)
        self.assertEqual(EXAMPLE['logical_source_port'],
                         sot.logical_source_port)
        self.assertEqual(EXAMPLE['logical_destination_port'],
                         sot.logical_destination_port)
        self.assertEqual(EXAMPLE['l7_parameters'], sot.l7_parameters)
