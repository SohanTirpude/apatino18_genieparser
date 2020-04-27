# Python
import unittest
from unittest.mock import Mock

# PyATS
from pyats.topology import (Device, loader)

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# junos show_arp
from genie.libs.parser.junos.show_ipv6_neighbors import ShowIpv6Neighbors


class TestShowIpv6Neighbors(unittest.TestCase):
    """ Unit tests for:
            * show ipv6 neighbors
    """

    device = Device(name='aDevice')
    maxDiff = None
    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': '''
        show ipv6 neighbors
        IPv6 Address                  Linklayer Address  State       Exp   Rtr  Secure  Interface               
        2001:268:fb8f:1f::1           00:50:56:8d:72:bd  reachable   28    yes  no      ge-0/0/1.0              
        fe80::250:56ff:fe8d:53c0      00:50:56:8d:53:c0  delay       4     yes  no      ge-0/0/0.0              
        fe80::250:56ff:fe8d:72bd      00:50:56:8d:72:bd  reachable   43    yes  no      ge-0/0/1.0              
        Total entries: 3
    '''}
    
    golden_parsed_output = {
        "ipv6-nd-information": {
            "ipv6-nd-entry": [
                {
                    "ipv6-nd-expire": "28",
                    "ipv6-nd-interface-name": "ge-0/0/1.0",
                    "ipv6-nd-isrouter": "yes",
                    "ipv6-nd-issecure": "no",
                    "ipv6-nd-neighbor-address": "2001:268:fb8f:1f::1",
                    "ipv6-nd-neighbor-l2-address": "00:50:56:8d:72:bd",
                    "ipv6-nd-state": "reachable"
                },
                {
                    "ipv6-nd-expire": "4",
                    "ipv6-nd-interface-name": "ge-0/0/0.0",
                    "ipv6-nd-isrouter": "yes",
                    "ipv6-nd-issecure": "no",
                    "ipv6-nd-neighbor-address": "fe80::250:56ff:fe8d:53c0",
                    "ipv6-nd-neighbor-l2-address": "00:50:56:8d:53:c0",
                    "ipv6-nd-state": "delay"
                },
                {
                    "ipv6-nd-expire": "43",
                    "ipv6-nd-interface-name": "ge-0/0/1.0",
                    "ipv6-nd-isrouter": "yes",
                    "ipv6-nd-issecure": "no",
                    "ipv6-nd-neighbor-address": "fe80::250:56ff:fe8d:72bd",
                    "ipv6-nd-neighbor-l2-address": "00:50:56:8d:72:bd",
                    "ipv6-nd-state": "reachable"
                }
            ],
            "ipv6-nd-total": "3"
        }
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6Neighbors(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

if __name__ == '__main__':
    unittest.main()