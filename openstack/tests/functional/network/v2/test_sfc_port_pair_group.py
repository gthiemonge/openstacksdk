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


from openstack.network.v2 import sfc_port_pair_group
from openstack.network.v2 import sfc_port_pair
from openstack.network.v2 import subnet
from openstack.network.v2 import network
from openstack.network.v2 import port
from openstack.tests.functional import base
from openstack import exceptions


class TestSfcPortPairGroup(base.BaseFunctionalTest):

    IPV4 = 4
    CIDR = "10.100.0.0/24"

    def require_networking_sfc(self):
        try:
            return [sot.id for sot in self.conn.network.sfc_port_pair_groups()]
        except exceptions.NotFoundException:
            self.skipTest('networking-sfc plugin not found in network')

    def setUp(self):
        super(TestSfcPortPairGroup, self).setUp()
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

        self.PPG_NAME = self.getUniqueString()
        self.UPDATE_NAME = self.getUniqueString()
        ppg = self.conn.network.create_sfc_port_pair_group(
            name=self.PPG_NAME,
            port_pairs=[self.PP1_ID])
        assert isinstance(ppg, sfc_port_pair_group.SfcPortPairGroup)
        self.PPG_ID = ppg.id

    def tearDown(self):
        self.conn.network.delete_sfc_port_pair_group(self.PPG_ID,
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
        super(TestSfcPortPairGroup, self).tearDown()

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
        sot = self.conn.network.get_sfc_port_pair_group(self.PPG_ID)
        self.assertEqual(self.PPG_ID, sot.id)
        self.assertIn(self.PP1_ID, sot.port_pairs)

    def test_list(self):
        ids = [sot.id for sot in self.conn.network.sfc_port_pair_groups()]
        self.assertIn(self.PPG_ID, ids)

    def test_find(self):
        sot = self.conn.network.find_sfc_port_pair_group(self.PPG_NAME)
        self.assertEqual(self.PPG_ID, sot.id)

    def test_update(self):
        sot = self.conn.network.update_sfc_port_pair_group(
            self.PPG_ID,
            name=self.UPDATE_NAME,
            port_pairs=[self.PP1_ID,
                        self.PP2_ID])
        self.assertEqual(self.UPDATE_NAME, sot.name)
        self.assertIn(self.PP1_ID, sot.port_pairs)
        self.assertIn(self.PP2_ID, sot.port_pairs)
