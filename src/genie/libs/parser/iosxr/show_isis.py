"""
show_isis.py

IOSXR parsers for the following show commands:
    * show isis adjacency
    * show isis neighbors

"""

# Python
import re
from netaddr import IPAddress, IPNetwork

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Or, Optional
from genie.libs.parser.utils.common import Common


#==================================
# Schema for 'show isis adjacency'
#==================================
class ShowIsisAdjacencySchema(MetaParser):
    """Schema for show run isis adjacency"""

    schema = {
        'isis': {
            Any(): {
                'vrf': {
                    Any(): {
                        'level': {
                            Any(): {
                                Optional('total_adjacency_count'): int,
                                Optional('interfaces'): {
                                    Any(): {
                                        'system_id': {
                                            Any(): {
                                                'interface': str,
                                                'snpa': str,
                                                'state': str,
                                                'hold': str,
                                                'changed': str,
                                                Optional('nsf'): str,
                                                Optional('bfd'): str,
                                                Optional('ipv4_bfd'): str,
                                                Optional('ipv6_bfd'): str,
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }


class ShowIsisAdjacency(ShowIsisAdjacencySchema):
    """Parser for show isis adjacency"""
    
    cli_command = 'show isis adjacency'
    
    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        
        ret_dict = {}
        vrf = 'default'

        # IS-IS p Level-1 adjacencies:
        p1 = re.compile(r'^IS-IS +(?P<isis_name>\w+) +(?P<level_name>\S+) adjacencies:$')

        # 12a4           PO0/1/0/1        *PtoP*         Up    23       00:00:06 Capable  None
        p2 = re.compile(r'^(?P<system_id>\S+) +(?P<interface>\S+) +(?P<snpa>\S+) +(?P<state>(Up|Down|None)) +(?P<hold>\S+) '
                         '+(?P<changed>\S+) +(?P<nsf>\S+) +(?P<bfd>(Up|Down|None|Init))$')

        # Total adjacency count: 1
        p3 = re.compile(r'^Total +adjacency +count: +(?P<adjacency_count>(\d+))$')

        # R1_xe          Gi0/0/0/0.115    fa16.3eab.a39d Up    26   22:30:26 Yes None None
        p4 = re.compile(r'^(?P<system_id>\S+) +(?P<interface>\S+) +(?P<snpa>\S+) +(?P<state>(Up|Down|None)) +(?P<hold>\S+) '
                         '+(?P<changed>\S+) +(?P<nsf>\S+) +(?P<ipv4_bfd>([\s\w]+)) +(?P<ipv6_bfd>([\w\s]+))$')

        for line in out.splitlines():
            line = line.strip()

            # IS-IS p Level-1 adjacencies:
            m = p1.match(line)
            if m:
                isis_name = m.groupdict()['isis_name']
                level_name = m.groupdict()['level_name']
                isis_adjacency_dict = ret_dict.setdefault('isis', {}).\
                                               setdefault(isis_name, {}).\
                                               setdefault('vrf', {}).\
                                               setdefault(vrf, {})

                level_dict = isis_adjacency_dict.setdefault('level', {}).setdefault(level_name, {})
                continue

            # 12a4           PO0/1/0/1        *PtoP*         Up    23       00:00:06 Capable  None
            m = p2.match(line)
            if m:
                system_id = m.groupdict()['system_id']
                interface = m.groupdict()['interface']
                interface_name = Common.convert_intf_name(m.groupdict()['interface'])
                snpa = m.groupdict()['snpa']
                state = m.groupdict()['state']
                hold = m.groupdict()['hold']
                changed = m.groupdict()['changed']
                nsf = m.groupdict()['nsf']
                bfd = m.groupdict()['bfd']
                interface_dict = level_dict.setdefault('interfaces', {}).setdefault(interface, {})
                system_dict = interface_dict.setdefault('system_id', {}).setdefault(system_id, {})
                system_dict['interface'] = interface_name
                system_dict['snpa'] = snpa
                system_dict['state'] = state
                system_dict['hold'] = hold
                system_dict['changed'] = changed
                system_dict['nsf'] = nsf
                system_dict['bfd'] = bfd
                continue

            # Total adjacency count: 1
            m = p3.match(line)
            if m:
                level_dict['total_adjacency_count'] = int(m.groupdict()['adjacency_count'])
                continue

            # R1_xe          Gi0/0/0/0.115    fa16.3eab.a39d Up    26   22:30:26 Yes None None
            m = p4.match(line)
            if m:
                system_id = m.groupdict()['system_id']
                interface = m.groupdict()['interface']
                interface_name = Common.convert_intf_name(m.groupdict()['interface'])
                snpa = m.groupdict()['snpa']
                state = m.groupdict()['state']
                hold = m.groupdict()['hold']
                changed = m.groupdict()['changed']
                nsf = m.groupdict()['nsf']
                ipv4_bfd = m.groupdict()['ipv4_bfd']
                ipv6_bfd = m.groupdict()['ipv6_bfd']
                interface_dict = level_dict.setdefault('interfaces', {}).setdefault(interface, {})
                system_dict = interface_dict.setdefault('system_id', {}).setdefault(system_id, {})
                system_dict['interface'] = interface_name
                system_dict['snpa'] = snpa
                system_dict['state'] = state
                system_dict['hold'] = hold
                system_dict['changed'] = changed
                system_dict['nsf'] = nsf
                system_dict['ipv4_bfd'] = ipv4_bfd
                system_dict['ipv6_bfd'] = ipv6_bfd
                continue

        return ret_dict


#======================================
# Schema for 'show isis neighbors'
#======================================
class ShowIsisNeighborsSchema(MetaParser):
    """Schema for show run isis neighbors"""

    schema = {
        'isis': {
            Any(): {
                'vrf': {
                    Any(): {
                        Optional('total_neighbor_count'): int,
                        Optional('interfaces'): {
                            Any(): {
                                'neighbors': {
                                    Any(): {
                                        'snpa': str,
                                        'state': str,
                                        'holdtime': str,
                                        'type': str,
                                        Optional('ietf_nsf'): str,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


class ShowIsisNeighbors(ShowIsisNeighborsSchema):
    """Parser for show isis neighbors"""
    
    cli_command = 'show isis neighbors'
    
    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        
        isis_neighbors_dict = {}
        vrf = 'default'

        # IS-IS 4445 neighbors:
        p1 = re.compile(r'^IS-IS\s+(?P<isis_name>\S+)\s*neighbors:$')

        # R1_xe          Gi0/0/0/0.115    fa16.3eab.a39d Up    24       L1L2 Capable
        p2 = re.compile(r'^(?P<system_id>\S+) +(?P<interface>\S+) +(?P<snpa>\S+) +(?P<state>(Up|Down|None)+) +(?P<holdtime>\S+) '
                         '+(?P<type>\S+) +(?P<ietf_nsf>\S+)$')

        # Total neighbor count: 1
        p3 = re.compile(r'^Total\sneighbor\scount:\s+(?P<neighbor_count>\S+)$')

        for line in out.splitlines():
            line = line.strip()

            # IS-IS 4445 neighbors:
            m = p1.match(line)
            if m:
                isis_name = m.groupdict()['isis_name']
                vrf_dict = isis_neighbors_dict.setdefault('isis', {}).\
                                               setdefault(isis_name, {}).\
                                               setdefault('vrf', {}).\
                                               setdefault(vrf, {})
                continue

            # R1_xe          Gi0/0/0/0.115    fa16.3eab.a39d Up    24       L1L2 Capable
            m = p2.match(line)
            if m:
                system_id = m.groupdict()['system_id']
                interface_name = Common.convert_intf_name(m.groupdict()['interface'])
                snpa = m.groupdict()['snpa']
                state = m.groupdict()['state']
                holdtime = m.groupdict()['holdtime']
                type = m.groupdict()['type']
                ietf_nsf = m.groupdict()['ietf_nsf']

                interface_dict = vrf_dict.setdefault('interfaces', {}).setdefault(interface_name, {})
                system_dict = interface_dict.setdefault('neighbors', {}).setdefault(system_id, {})
                system_dict['snpa'] = snpa
                system_dict['state'] = state
                system_dict['holdtime'] = holdtime
                system_dict['type'] = type
                system_dict['ietf_nsf'] = ietf_nsf

                continue
            
            # Total neighbor count: 1
            m = p3.match(line)
            if m:
                vrf_dict['total_neighbor_count'] = int(m.groupdict()['neighbor_count'])
                continue

        return isis_neighbors_dict


# ======================================================
#  Schema for 'show isis segment-routing label table'
# ======================================================
class ShowIsisSegmentRoutingLabelTableSchema(MetaParser):
    """Schema for show isis segment-routing label table"""

    schema = {
        'instance': {
            'SR': {
                'label': {
                    Any(): {
                        'prefix_interface': str,
                    },
                }
            }
        }
    }


class ShowIsisSegmentRoutingLabelTable(ShowIsisSegmentRoutingLabelTableSchema):
    """Parser for show isis segment-routing label table"""
    
    cli_command = ['show isis segment-routing label table']
    
    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command[0])
        else:
            out = output
        
        isis_dict = {}

        # IS-IS SR IS Label Table
        p1 = re.compile(r'^IS-IS\s+(?P<instance>\S+)\s+IS\s+Label\s+Table$')

        # Label         Prefix/Interface
        # ----------    ----------------
        # 16001         Loopback0
        # 16002         10.2.2.2/32
        p2 = re.compile(r'^(?P<label>\d+)\s+(?P<prefix_interface>\S+)$')

        for line in out.splitlines():
            line = line.strip()

            # IS-IS SR IS Label Table
            m = p1.match(line)
            if m:
                instance = m.groupdict()['instance']
                final_dict = isis_dict.setdefault('instance', {}).\
                    setdefault(instance, {})
                continue

            # Label         Prefix/Interface
            # ----------    ----------------
            # 16001         Loopback0
            # 16002         10.2.2.2/32
            m = p2.match(line)
            if m:
                label = int(m.groupdict()['label'])
                prefix_interface = m.groupdict()['prefix_interface']
                final_dict.setdefault('label', {}).setdefault(
                    label, {}).update(
                    {'prefix_interface': prefix_interface})
                continue

        return isis_dict

class ShowIsisHostnameSchema(MetaParser):
    ''' Schema for commands:
        * show isis hostname
    '''

    schema = {
        'isis': {
            Any(): {
                'vrf': {
                    Any(): {
                        'level': {
                            Any(): {
                                'hostname': {
                                    Any(): {
                                        'system_id': str,
                                        Optional('local_router'): bool
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

class ShowIsisHostname(ShowIsisHostnameSchema):
    ''' Parser for commands:
        * show isis hostname
    '''

    cli_command = 'show hostname'

    def cli(self, output=None):

        if output is None:
            output = self.device.execute(self.cli_command)

        # IS-IS TEST1 hostnames
        r1 = re.compile(r'IS\-IS\s(?P<isis>.+)\s+hostnames')

        # 2     1720.1800.0254 tor-28.tenlab-cloud
        # 2     1720.1800.0213 leaf-2.qa-site1
        # 2     1720.1800.0250 tor-23.tenlab-cloud
        r2 = re.compile(r'(?P<level>[\d\,]+)\s+(?P<local_router>\**)\s+(?P<system_id>\S+)\s+(?P<dynamic_hostname>\S+)')

        parsed_output = {}
        vrf = 'default'

        for line in output.splitlines():
            line = line.strip()
            
            # IS-IS TEST1 hostnames            
            result = r1.match(line)
            if result:                
                group = result.groupdict()
                isis = group['isis']

                isis_dict = parsed_output\
                    .setdefault('isis', {})\
                    .setdefault(isis, {})\
                    .setdefault('vrf', {})\
                    .setdefault(vrf, {})                    

                continue

            # 2     1720.1800.0254 tor-28.tenlab-cloud
            # 2     1720.1800.0213 leaf-2.qa-site1
            # 2     1720.1800.0250 tor-23.tenlab-cloud            
            result = r2.match(line)
            if result:
                group = result.groupdict()

                levels = group['level']
                system_id = group['system_id']
                local_router = group.get('local_router', None)
                dynamic_hostname = group['dynamic_hostname']

                for level in levels.split(','):
                    hostname_dict = isis_dict\
                        .setdefault('level', {})\
                        .setdefault(int(level), {})\
                        .setdefault('hostname', {})\
                        .setdefault(dynamic_hostname, {})\

                    hostname_dict['system_id'] = system_id
                    if local_router:
                        hostname_dict['local_router'] = True

                continue

        return parsed_output
