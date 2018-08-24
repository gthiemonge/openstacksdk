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


from openstack.network.v2 import sfc_port_pair
from openstack.network.v2 import subnet
from openstack.network.v2 import network
from openstack.network.v2 import port
from openstack.tests.functional import base
from openstack import exceptions


class TestSfcPortPair(base.BaseFunctionalTest):

    IPV4 = 4
    CIDR = "10.100.0.0/24"

    SERVICE_FUNCTION_PARAMETERS = {'correlation': 'nsh'}

    def require_networking_sfc(self):
        try:
            return [sot.id for sot in self.conn.network.sfc_port_pairs()]
        except exceptions.NotFoundException:
            self.skipTest('networking-sfc plugin not found in network')

    def setUp(self):
        super(TestSfcPortPair, self).setUp()
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

        self.PP_NAME = self.getUniqueString()
        self.UPDATE_NAME = self.getUniqueString()
        pp = self.conn.network.create_sfc_port_pair(
            name=self.PP_NAME,
            ingress=self.PORT1_ID,
            egress=self.PORT2_ID,
            service_function_parameters=self.SERVICE_FUNCTION_PARAMETERS)
        assert isinstance(pp, sfc_port_pair.SfcPortPair)
        self.PP_ID = pp.id

    def tearDown(self):
        self.conn.network.delete_sfc_port_pair(self.PP_ID,
                                               ignore_missing=False)
        self.conn.compute.delete_server(self.SERVER_ID, ignore_missing=False)
        self.conn.network.delete_port(self.PORT1_ID, ignore_missing=False)
        self.conn.network.delete_port(self.PORT2_ID, ignore_missing=False)
        self.conn.network.delete_subnet(self.SUB_ID, ignore_missing=False)
        self.conn.network.delete_network(self.NET_ID, ignore_missing=False)
        super(TestSfcPortPair, self).tearDown()

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
        sot = self.conn.network.get_sfc_port_pair(self.PP_ID)
        self.assertEqual(self.PORT1_ID, sot.ingress)
        self.assertEqual(self.PORT2_ID, sot.egress)
        for k in self.SERVICE_FUNCTION_PARAMETERS:
            self.assertEqual(self.SERVICE_FUNCTION_PARAMETERS[k],
                             sot.service_function_parameters[k])

    def test_list(self):
        ids = [sot.id for sot in self.conn.network.sfc_port_pairs()]
        self.assertIn(self.PP_ID, ids)

    def test_find(self):
        sot = self.conn.network.find_sfc_port_pair(self.PP_NAME)
        self.assertEqual(self.PP_ID, sot.id)

    def test_update(self):
        sot = self.conn.network.update_sfc_port_pair(
            self.PP_ID,
            name=self.UPDATE_NAME)
        self.assertEqual(self.UPDATE_NAME, sot.name)
