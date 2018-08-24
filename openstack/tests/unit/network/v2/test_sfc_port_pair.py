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

from openstack.network.v2 import sfc_port_pair

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'description': '1',
    'name': '2',
    'tenant_id': '3',
    'ingress': '4',
    'egress': '5',
    'service_function_parameters': {'6': '6'},
}


class TestSfcPortPair(testtools.TestCase):

    def test_basic(self):
        sot = sfc_port_pair.SfcPortPair()
        self.assertEqual('port_pair', sot.resource_key)
        self.assertEqual('port_pairs', sot.resources_key)
        self.assertEqual('/sfc/port_pairs', sot.base_path)
        self.assertEqual('network', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({"description": "description",
                              "name": "name",
                              "project_id": "tenant_id",
                              "ingress": "ingress",
                              "egress": "egress",
                              "service_function_parameters":
                                  "service_function_parameters",
                              "limit": "limit",
                              "marker": "marker"},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = sfc_port_pair.SfcPortPair(**EXAMPLE)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
        self.assertEqual(EXAMPLE['ingress'], sot.ingress)
        self.assertEqual(EXAMPLE['egress'], sot.egress)
        self.assertEqual(EXAMPLE['service_function_parameters'],
                         sot.service_function_parameters)
