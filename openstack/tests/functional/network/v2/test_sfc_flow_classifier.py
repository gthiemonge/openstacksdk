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


from openstack.network.v2 import sfc_flow_classifier
from openstack.network.v2 import subnet
from openstack.network.v2 import network
from openstack.network.v2 import port
from openstack.tests.functional import base
from openstack import exceptions


class TestSfcFlowClassifier(base.BaseFunctionalTest):

    IPV4 = 4
    CIDR = "10.100.0.0/24"

    def require_networking_sfc(self):
        try:
            return [sot.id for sot in self.conn.network.sfc_flow_classifiers()]
        except exceptions.NotFoundException:
            self.skipTest('networking-sfc plugin not found in network')

    def setUp(self):
        super(TestSfcFlowClassifier, self).setUp()
        self.require_networking_sfc()

        name = self.getUniqueString()
        net = self._create_network(name)
        self.NET_ID = net.id

        name = self.getUniqueString()
        sub = self._create_subnet(name, net.id, self.CIDR)
        self.SUB_ID = sub.id

        p1 = self.conn.network.create_port(network_id=self.NET_ID)
        assert isinstance(p1, port.Port)
        self.PORT1_ID = p1.id

        self.FC_NAME = self.getUniqueString()
        self.UPDATE_NAME = self.getUniqueString()
        fc = self.conn.network.create_sfc_flow_classifier(
            name=self.FC_NAME,
            logical_source_port=self.PORT1_ID,
            source_ip_prefix=self.CIDR)
        assert isinstance(fc, sfc_flow_classifier.SfcFlowClassifier)
        self.FC_ID = fc.id

    def tearDown(self):
        self.conn.network.delete_sfc_flow_classifier(self.FC_ID,
                                                     ignore_missing=False)
        self.conn.network.delete_port(self.PORT1_ID, ignore_missing=False)
        self.conn.network.delete_subnet(self.SUB_ID, ignore_missing=False)
        self.conn.network.delete_network(self.NET_ID, ignore_missing=False)
        super(TestSfcFlowClassifier, self).tearDown()

    def _create_subnet(self, name, net_id, cidr):
        self.name = name
        self.net_id = net_id
        self.cidr = cidr
        sub = self.conn.network.create_subnet(
            name=self.name,
            ip_version=self.IPV4,
            network_id=self.net_id,
            cidr=self.cidr)
        assert isinstance(sub, subnet.Subnet)
        self.assertEqual(self.name, sub.name)
        return sub

    def _create_network(self, name, **args):
        self.name = name
        net = self.conn.network.create_network(name=name, **args)
        assert isinstance(net, network.Network)
        self.assertEqual(self.name, net.name)
        return net

    def test_get(self):
        sot = self.conn.network.get_sfc_flow_classifier(self.FC_ID)
        self.assertEqual(self.PORT1_ID, sot.logical_source_port)
        self.assertEqual(self.CIDR, sot.source_ip_prefix)
        self.assertEqual(None, sot.destination_ip_prefix)

    def test_list(self):
        ids = [sot.id for sot in self.conn.network.sfc_flow_classifiers()]
        self.assertIn(self.FC_ID, ids)

    def test_find(self):
        sot = self.conn.network.find_sfc_flow_classifier(self.FC_NAME)
        self.assertEqual(self.FC_ID, sot.id)

    def test_update(self):
        sot = self.conn.network.update_sfc_flow_classifier(
            self.FC_ID,
            name=self.UPDATE_NAME)
        self.assertEqual(self.UPDATE_NAME, sot.name)
