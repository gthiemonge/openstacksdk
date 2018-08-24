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


from openstack.network.v2 import sfc_port_chain
from openstack.network.v2 import sfc_flow_classifier
from openstack.network.v2 import sfc_port_pair_group
from openstack.network.v2 import sfc_port_pair
from openstack.network.v2 import subnet
from openstack.network.v2 import network
from openstack.network.v2 import port
from openstack.tests.functional import base
from openstack import exceptions


class TestSfcPortChain(base.BaseFunctionalTest):

    IPV4 = 4
    CIDR = "10.100.0.0/24"

    CHAIN_PARAMETERS = {'correlation': 'nsh'}

    def require_networking_sfc(self):
        try:
            return [sot.id for sot in self.conn.network.sfc_port_chains()]
        except exceptions.NotFoundException:
            self.skipTest('networking-sfc plugin not found in network')

    def setUp(self):
        super(TestSfcPortChain, self).setUp()
        self.require_networking_sfc()

        name = self.getUniqueString()
        net = self._create_network(name)
        self.NET_ID = net.id

        name = self.getUniqueString()
        sub = self._create_subnet(name, net.id, self.CIDR)
        self.SUB_ID = sub.id

        self.PORT1_ID = None
        self.PORT2_ID = None
        self.SERVER_ID = None

        self._create_server()

        name = self.getUniqueString()
        pp1 = self.conn.network.create_sfc_port_pair(
            name=name,
            ingress=self.PORT1_ID,
            egress=self.PORT2_ID)
        assert isinstance(pp1, sfc_port_pair.SfcPortPair)
        self.PP1_ID = pp1.id

        name = self.getUniqueString()
        pp2 = self.conn.network.create_sfc_port_pair(
            name=name,
            ingress=self.PORT2_ID,
            egress=self.PORT1_ID)
        assert isinstance(pp2, sfc_port_pair.SfcPortPair)
        self.PP2_ID = pp2.id

        self.PPG1_NAME = self.getUniqueString()
        ppg1 = self.conn.network.create_sfc_port_pair_group(
            name=self.PPG1_NAME,
            port_pairs=[self.PP1_ID])
        assert isinstance(ppg1, sfc_port_pair_group.SfcPortPairGroup)
        self.PPG1_ID = ppg1.id

        self.PPG2_NAME = self.getUniqueString()
        ppg2 = self.conn.network.create_sfc_port_pair_group(
            name=self.PPG2_NAME,
            port_pairs=[self.PP2_ID])
        assert isinstance(ppg2, sfc_port_pair_group.SfcPortPairGroup)
        self.PPG2_ID = ppg2.id

        self.FC_NAME = self.getUniqueString()
        fc = self.conn.network.create_sfc_flow_classifier(
            name=self.FC_NAME,
            logical_source_port=self.PORT1_ID,
            source_ip_prefix=self.CIDR)
        assert isinstance(fc, sfc_flow_classifier.SfcFlowClassifier)
        self.FC_ID = fc.id

        self.PC_NAME = self.getUniqueString()
        self.UPDATE_NAME = self.getUniqueString()
        pc = self.conn.network.create_sfc_port_chain(
            name=self.PC_NAME,
            port_pair_groups=[self.PPG1_ID, self.PPG2_ID],
            flow_classifiers=[self.FC_ID],
            chain_parameters=self.CHAIN_PARAMETERS)
        assert isinstance(pc, sfc_port_chain.SfcPortChain)
        self.PC_ID = pc.id

    def tearDown(self):
        self.conn.network.delete_sfc_port_chain(self.PC_ID,
                                                ignore_missing=False)
        self.conn.network.delete_sfc_flow_classifier(self.FC_ID,
                                                     ignore_missing=False)
        self.conn.network.delete_sfc_port_pair_group(self.PPG1_ID,
                                                     ignore_missing=False)
        self.conn.network.delete_sfc_port_pair_group(self.PPG2_ID,
                                                     ignore_missing=False)
        self.conn.network.delete_sfc_port_pair(self.PP1_ID,
                                               ignore_missing=False)
        self.conn.network.delete_sfc_port_pair(self.PP2_ID,
                                               ignore_missing=False)
        self.conn.compute.delete_server(self.SERVER_ID, ignore_missing=False)
        self.conn.network.delete_port(self.PORT1_ID, ignore_missing=False)
        self.conn.network.delete_port(self.PORT2_ID, ignore_missing=False)
        self.conn.network.delete_subnet(self.SUB_ID, ignore_missing=False)
        self.conn.network.delete_network(self.NET_ID, ignore_missing=False)
        super(TestSfcPortChain, self).tearDown()

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

    def _create_server(self):
        p1 = self.conn.network.create_port(network_id=self.NET_ID)
        assert isinstance(p1, port.Port)
        self.PORT1_ID = p1.id

        p2 = self.conn.network.create_port(network_id=self.NET_ID)
        assert isinstance(p2, port.Port)
        self.PORT2_ID = p2.id

        flavor = self.conn.compute.find_flavor(base.FLAVOR_NAME,
                                               ignore_missing=False)
        image = self.conn.compute.find_image(base.IMAGE_NAME,
                                             ignore_missing=False)
        srv = self.conn.compute.create_server(
            name=self.getUniqueString(),
            flavor_id=flavor.id, image_id=image.id,
            networks=[{"port": self.PORT1_ID}, {"port": self.PORT2_ID}])
        self.conn.compute.wait_for_server(srv)

        self.SERVER_ID = srv.id

    def test_get(self):
        sot = self.conn.network.get_sfc_port_chain(self.PC_ID)
        self.assertEqual(self.PC_ID, sot.id)
        self.assertIn(self.PPG1_ID, sot.port_pair_groups)
        self.assertIn(self.PPG2_ID, sot.port_pair_groups)
        self.assertIn(self.FC_ID, sot.flow_classifiers)
        for k in self.CHAIN_PARAMETERS:
            self.assertEqual(self.CHAIN_PARAMETERS[k],
                             sot.chain_parameters[k])

    def test_list(self):
        ids = [sot.id for sot in self.conn.network.sfc_port_chains()]
        self.assertIn(self.PC_ID, ids)

    def test_find(self):
        sot = self.conn.network.find_sfc_port_chain(self.PC_NAME)
        self.assertEqual(self.PC_ID, sot.id)

    def test_update(self):
        sot = self.conn.network.update_sfc_port_chain(
            self.PC_ID,
            name=self.UPDATE_NAME,
            port_pair_groups=[self.PPG1_ID],
            flow_classifiers=[self.FC_ID])
        self.assertEqual(self.UPDATE_NAME, sot.name)
        self.assertIn(self.PPG1_ID, sot.port_pair_groups)
        self.assertNotIn(self.PPG2_ID, sot.port_pair_groups)
        self.assertIn(self.FC_ID, sot.flow_classifiers)
