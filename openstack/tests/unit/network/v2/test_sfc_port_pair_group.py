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

from openstack.network.v2 import sfc_port_pair_group

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'description': '1',
    'name': '2',
    'tenant_id': '3',
    'port_pairs': ['4'],
    'port_pair_group_parameters': {'5': '5'},
}


class TestSfcPortPairGroup(testtools.TestCase):

    def test_basic(self):
        sot = sfc_port_pair_group.SfcPortPairGroup()
        self.assertEqual('port_pair_group', sot.resource_key)
        self.assertEqual('port_pair_groups', sot.resources_key)
        self.assertEqual('/sfc/port_pair_groups', sot.base_path)
        self.assertEqual('network', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({"description": "description",
                              "name": "name",
                              "project_id": "tenant_id",
                              "port_pairs": "port_pairs",
                              "port_pair_group_parameters":
                                  "port_pair_group_parameters",
                              "limit": "limit",
                              "marker": "marker"},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = sfc_port_pair_group.SfcPortPairGroup(**EXAMPLE)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
        self.assertEqual(EXAMPLE['port_pairs'], sot.port_pairs)
        self.assertEqual(EXAMPLE['port_pair_group_parameters'],
                         sot.port_pair_group_parameters)
