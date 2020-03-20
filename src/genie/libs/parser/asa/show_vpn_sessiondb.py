"""
show_vpn_sessiondb.py

Parser for the following show commands:
    * show vpn load-balancing
    * show vpn-sessiondb summary
    * show vpn-sessiondb
    * show vpn-sessiondb anyconnect
    * show vpn-sessiondb anyconnect sort inactivity
    * show vpn-sessiondb webvpn
"""


import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, \
                                                Any, \
                                                Optional


# =============================================
# Schema for 'show vpn-sessiondb summary'
# =============================================
class ShowVPNSessionDBSummarySchema(MetaParser):
    """Schema for
        * show vpn-sessiondb summary
    """

    schema = {
        Optional('ikev1_ipsec_l2tp_ip_sec'): {
            'active': int,
            'cumulative': int,
            'peak_concurrent': int,
            Optional('inactive'): int,
        },
        Optional('load_balancing_encryption'): {
            'active': int,
            'cumulative': int,
            'peak_concurrent': int,
            Optional('inactive'): int,
        },
        Optional('anyconnect_client'): {
            'active': int,
            'cumulative': int,
            'peak_concurrent': int,
            Optional('inactive'): int,
            Optional('ssl_tls_dtls'): {
                'active': int,
                'cumulative': int,
                'peak_concurrent': int,
                Optional('inactive'): int,
            }
        },
        Optional('clientless_vpn'): {
            'active': int,
            'cumulative': int,
            'peak_concurrent': int,
            Optional('inactive'): int,
            Optional('browser'): {
                'active': int,
                'cumulative': int,
                'peak_concurrent': int,
                Optional('inactive'): int,
            }
        },
        'total_active_and_inactive': int,
        'total_cumulative': int,
        Optional('device_total_vpn_capacity'): int,
        Optional('device_load'): float,
    }


# =============================================
# Parser for 'show vpn-sessiondb summary'
# =============================================
class ShowVPNSessionDBSummary(ShowVPNSessionDBSummarySchema):
    """Parser for
        * show vpn-sessiondb summary
    """

    cli_command = 'show vpn-sessiondb summary'

    def cli(self, output=None):
        if output is None:
            # excute command to get output
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        # IKEv1 IPsec/L2TP IPsec       :      2 :          2 :           2
        p1 = re.compile(r'^IKEv1 +IPsec\/L2TP +IPsec +: +(?P<active>\d+) *'
                        r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                        r'( *: (?P<inactive>\d+))?$')

        # Load Balancing(Encryption)   :      0 :          6 :           1
        p2 = re.compile(r'^Load +Balancing\(Encryption\) +: +(?P<active>\d+) *'
                        r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                        r'( *: (?P<inactive>\d+))?$')

        # Total Active and Inactive    :      2             Total Cumulative :      8
        p3 = re.compile(r'^Total +Active +and +Inactive +: +'
                        r'(?P<total_active_and_inactive>\d+) +Total +Cumulative +: +'
                        r'(?P<total_cumulative>\d+)$')

        # Device Total VPN Capacity    :    250
        p4 = re.compile(r'^Device +Total +VPN +Capacity +: +'
                        r'(?P<device_total_vpn_capacity>\d+)$')

        # Device Load                  :     1%
        p5 = re.compile(r'^Device +Load +: +(?P<device_load>\d+)\%$')

        # AnyConnect Client            :    127 :        432 :         205 :        0
        p6 = re.compile(r'^AnyConnect Client +: +(?P<active>\d+) *'
                        r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                        r' *: +(?P<inactive>\d+)$')

        # SSL/TLS/DTLS               :    127 :        432 :         205 :        0
        p7 = re.compile(r'^SSL/TLS/DTLS +: +(?P<active>\d+) *'
                        r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                        r' *: +(?P<inactive>\d+)$')

        # Clientless VPN               :   2    :     125    :            6
        p8 = re.compile(r'^Clientless VPN +: +(?P<active>\d+) *'
                        r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                        r'( *: +(?P<inactive>\d+))?$')

        # Browser                    :   2    :     125    :            6
        p9 = re.compile(r'^Browser +: +(?P<active>\d+) *'
                        r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                        r'( *: +(?P<inactive>\d+))?$')

        for line in out.splitlines():
            line = line.strip()

            # IKEv1 IPsec/L2TP IPsec       :      2 :          2 :           2
            m = p1.match(line)
            if m:
                group = m.groupdict()
                active = int(group['active'])
                cumulative = int(group['cumulative'])
                peak_concurrent = int(group['peak_concurrent'])
                inactive = group.get('inactive', None)
                ikev1_ipsec_l2tp_ip_sec_dict = ret_dict.setdefault('ikev1_ipsec_l2tp_ip_sec', {})
                ikev1_ipsec_l2tp_ip_sec_dict.update({'active': active})
                ikev1_ipsec_l2tp_ip_sec_dict.update({'cumulative': cumulative})
                ikev1_ipsec_l2tp_ip_sec_dict.update({'peak_concurrent': peak_concurrent})
                if inactive:
                    ikev1_ipsec_l2tp_ip_sec_dict.update({'inactive': int(inactive)})
                continue

            # Load Balancing(Encryption)   :      0 :          6 :           1
            m = p2.match(line)
            if m:
                group = m.groupdict()
                active = int(group['active'])
                cumulative = int(group['cumulative'])
                peak_concurrent = int(group['peak_concurrent'])
                inactive = group.get('inactive', None)
                load_balancing_encryption_dict = ret_dict.setdefault('load_balancing_encryption', {})
                load_balancing_encryption_dict.update({'active': active})
                load_balancing_encryption_dict.update({'cumulative': cumulative})
                load_balancing_encryption_dict.update({'peak_concurrent': peak_concurrent})
                if inactive:
                    load_balancing_encryption_dict.update({'inactive': int(inactive)})
                continue

            # AnyConnect Client            :    127 :        432 :         205 :        0
            m = p6.match(line)
            if m:
                group = m.groupdict()
                if 'anyconnect_client' not in ret_dict:
                    anyconnect_client_dict = ret_dict.setdefault('anyconnect_client', {})

                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    anyconnect_client_dict[k] = int(group[k])

                continue

            # SSL/TLS/DTLS               :    127 :        432 :         205 :        0
            m = p7.match(line)
            if m:
                group = m.groupdict()
                ssl_dict = anyconnect_client_dict.setdefault('ssl_tls_dtls', {})
                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    if group[k]:
                        ssl_dict[k] = int(group[k])
                continue

            # Clientless VPN               :   2    :     125    :            6
            m = p8.match(line)
            if m:
                group = m.groupdict()
                if 'clientless_vpn' not in ret_dict:
                    clientless_vpn_dict = ret_dict.setdefault('clientless_vpn', {})

                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    if group[k]:
                        clientless_vpn_dict[k] = int(group[k])

                continue

            # Browser                    :   2    :     125    :            6
            m = p9.match(line)
            if m:
                group = m.groupdict()
                browser_dict = clientless_vpn_dict.setdefault('browser', {})
                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    if group[k]:
                        browser_dict[k] = int(group[k])
                continue

            # Total Active and Inactive    :      2             Total Cumulative :      8
            m = p3.match(line)
            if m:
                group = m.groupdict()
                total_active_and_inactive = int(group['total_active_and_inactive'])
                total_cumulative = int(group['total_cumulative'])
                ret_dict.update({'total_active_and_inactive': total_active_and_inactive})
                ret_dict.update({'total_cumulative': total_cumulative})
                continue

            # Device Total VPN Capacity    :    250
            m = p4.match(line)
            if m:
                group = m.groupdict()
                device_total_vpn_capacity = int(group['device_total_vpn_capacity'])
                ret_dict.update({'device_total_vpn_capacity': device_total_vpn_capacity})
                continue

            # Device Load                  :     1%
            m = p5.match(line)
            if m:
                group = m.groupdict()
                device_load = int(group['device_load'])/100
                ret_dict.update({'device_load': device_load})
                continue

        return ret_dict

# =============================================
# Schema for
#     * show vpn-sessiondb
#     * show vpn-sessiondb anyconnect
#     * show vpn-sessiondb anyconnect sort inactivity
#     * show vpn-sessiondb webvpn
# =============================================


class ShowVpnSessiondbSchema(MetaParser):
    schema = {
        Optional('session_type'): {
            Any(): {
                'username': {
                    Any(): {
                        'index': {
                            int: {
                                Optional('ip_addr'): str,
                                Optional('assigned_ip'): str,
                                Optional('public_ip'): str,
                                'protocol': str,
                                Optional('vpn_client_encryption'): str,
                                Optional('license'): str,
                                Optional('encryption'): str,
                                'hashing': str,
                                Optional('ssl_tunnel'): str,
                                Optional('dtls_tunnel'): str,
                                Optional('auth_mode'): str,
                                Optional('group_policy'): str,
                                Optional('group'): str,
                                Optional('tunnel_group'): str,
                                Optional('tcp'): {
                                    'src_port': int,
                                    'dst_port': int,
                                },
                                'bytes': {
                                    'tx': int,
                                    'rx': int,
                                },
                                Optional('pkts'): {
                                    'tx': int,
                                    'rx': int,
                                },

                                Optional('client_version'): str,
                                Optional('client_type'): str,
                                Optional('nac_result'): str,
                                'login_time': str,
                                'duration': str,
                                'inactivity': str,
                                Optional('filter_name'): str,
                                Optional('vlan_mapping'): str,
                                Optional('vlan'): str,
                                Optional('audt_sess_id'): str,
                                Optional('security_group'): str,

                            }
                        }
                    }
                }
            }
        },
        Optional('summary'): {
            'vpn_session': {
                'total_active_and_inactive': int,
                'total_cumulative': int,
                Optional('device_total_vpn_capacity'): int,
                Optional('device_load'): float,
                Optional('anyconnect_client'): {
                    'active': int,
                    'cumulative': int,
                    'peak_concurrent': int,
                    Optional('inactive'): int,
                    Optional('ssl_tls_dtls'): {
                        'active': int,
                        'cumulative': int,
                        'peak_concurrent': int,
                        Optional('inactive'): int,
                    },
                },
                Optional('clientless_vpn'): {
                    'active': int,
                    'cumulative': int,
                    'peak_concurrent': int,
                    Optional('inactive'): int,
                    Optional('browser'): {
                        'active': int,
                        'cumulative': int,
                        'peak_concurrent': int,
                        Optional('inactive'): int,
                    },
                },
            },
            'tunnels': {
                'anyconnect_parent': {
                    'active': int,
                    'cumulative': int,
                    'peak_concurrent': int,
                    Optional('inactive'): int,
                },
                'ssl_tunnel': {
                    'active': int,
                    'cumulative': int,
                    'peak_concurrent': int,
                    Optional('inactive'): int,
                },
                'dtls_tunnel': {
                    'active': int,
                    'cumulative': int,
                    'peak_concurrent': int,
                    Optional('inactive'): int,
                },
                'totals': {
                    'active': int,
                    'cumulative': int,
                    Optional('peak_concurrent'): int,
                    Optional('inactive'): int,
                }
            }
        }
    }

# =============================================
# Super Parser for
#         * show vpn-sessiondb
#         * show vpn-sessiondb anyconnect
#         * show vpn-sessiondb anyconnect sort inactivity
#         * show vpn-sessiondb webvpn
# =============================================


class ShowVpnSessiondbSuper(ShowVpnSessiondbSchema):
    """Super Parser for
        * show vpn-sessiondb
        * show vpn-sessiondb anyconnect
        * show vpn-sessiondb anyconnect sort inactivity
        * show vpn-sessiondb webvpn
    """

    def cli(self, sort=None, output=None):

        parsed_dict = {}

        # --------------------------------------------------------------------
        # Regular expression patterns
        # --------------------------------------------------------------------

        # Session Type: SSL VPN Client
        p1 = re.compile(r'^Session\s+Type:\s+(?P<session_type>[\s\S]+)$')

        # Username : lee
        # Username : lee Index : 1
        p2 = re.compile(r'^Username\s+:\s+(?P<username>\S+)'
                        r'(\s+Index\s+:\s+(?P<index>\d+))?$')

        # Index : 1 IP Addr : 192.168.16.232
        p3 = re.compile(r'^Index\s+:\s+(?P<index>\d+)\s+'
                        r'IP\s+Addr\s+:\s+(?P<ip_addr>\S+)$')

        # Protocol : SSL VPN Client Encryption : 3DES
        # Protocol : AnyConnect-Parent SSL-Tunnel DTLS-Tunnel
        p4 = re.compile(r'^Protocol\s+:\s(?P<protocol>[-\w\s]+)(\s+'
                        r'VPN\s+Client\s+Encryption\s+:'
                        r'\s+(?P<vpn_client_encryption>\S+))?$')

        # Hashing : SHA1 Auth Mode : userPassword
        p5 = re.compile(r'^Hashing\s+:\s+(?P<hashing>\S+)\s+'
                        r'Auth\s+Mode\s+:\s+(?P<auth_mode>\S+)$')

        # Hashing : AnyConnect-Parent: (1)none
        p5_1 = re.compile(r'^Hashing\s+:\s+(?P<protocol>\S+):\s+(?P<hashing>\S+)$')

        # TCP Dst Port : 443 TCP Src Port : 54230
        p6 = re.compile(r'^TCP\s+Dst\s+Port\s+:\s+(?P<dst_port>\d+)\s+'
                        r'TCP\s+Src\s+Port\s+:\s+(?P<src_port>\d+)$')

        # Bytes Tx : 20178 Bytes Rx : 8662
        # Pkts Tx : 27 Pkts Rx : 19
        p7 = re.compile(r'^(?P<type>Bytes|Pkts)\s+Tx\s+:\s+(?P<tx>\d+)\s+'
                        r'(?P<type2>Bytes|Pkts)\s+Rx\s+:\s+(?P<rx>\d+)$')

        # Client Ver : Cisco STC 10.4.0.117
        p9 = re.compile(r'^Client\s+Ver\s+:\s+(?P<client_version>[\s\S]+)$')

        # Client Type : Internet Explorer
        p10 = re.compile(r'^Client\s+Type\s+:\s+(?P<client_type>[\s\S]+)$')

        # Group : DfltGrpPolicy
        p11 = re.compile(r'^Group\s+:\s+(?P<group>\S+)$')

        # Login Time : 14:32:03 UTC Wed Mar 20 2007
        p12 = re.compile(r'^Login\s+Time\s+:\s+(?P<login_time>[\s\S]+)$')

        # Duration : 0h:00m:04s
        # Duration : 2d 4h:21m:44s
        p13 = re.compile(r'^Duration\s+:\s+(?P<duration>[\s\S]+)$')

        # Inactivity : 0h:00m:04s
        # Inactivity : 1d 9h:13m:24s
        p14 = re.compile(r'^Inactivity\s+:\s+(?P<inactivity>[\s\S]+)$')

        # Filter Name :
        p15 = re.compile(r'^Filter\s+Name\s+:\s+(?P<filter_name>\S+)$')

        # Assigned IP : 192.168.246.2 Public IP : 10.139.1.3
        p16 = re.compile(r'^Assigned\s+IP\s+:\s+(?P<assigned_ip>\S+)\s+'
                         r'Public\s+IP\s+:\s+(?P<public_ip>\S+)$')

        # License : AnyConnect Premium
        p17 = re.compile(r'^License\s+:\s+(?P<license>[\s\S]+)$')

        # Encryption : RC4 AES128 Hashing : SHA1
        p18 = re.compile(r'^Encryption\s+:\s+(?P<encryption>[\s\S]+)\s+'
                         r'Hashing\s+:\s+(?P<hashing>\S+)$')

        # Encryption : AnyConnect-Parent: (1)none
        # Encryption   : Clientless: (1)AES128  Hashing      : Clientless: (1)SHA256
        p18_1 = re.compile(r'^Encryption\s+:\s+(?P<protocol>\S+):'
                           r'\s+(?P<encryption>\S+)(\s+Hashing\s+:'
                           r'\s+(?P<protocol2>\S+):\s+(?P<hashing>\S+))?$')

        # Group Policy : EngPolicy Tunnel Group : EngGroup
        # Group Policy : GroupPolicy_Employee
        # Tunnel Group : Employee
        p19 = re.compile(r'^(Group\s+Policy\s+:\s+(?P<group_policy>\S+))?'
                         r'(\s*Tunnel\s+Group\s+:\s+(?P<tunnel_group>\S+))?$')

        # NAC Result : Unknown
        p20 = re.compile(r'^NAC\s+Result\s+:\s+(?P<nac_result>\S+)$')

        # VLAN Mapping : N/A VLAN : none
        p21 = re.compile(r'^VLAN\s+Mapping\s+:\s+(?P<vlan_mapping>\S+)\s+'
                         r'VLAN\s+:\s+(?P<vlan>\S+)$')

        # Audt Sess ID : 0adc27fd093260005381
        p22 = re.compile(r'^Audt\s+Sess\s+ID\s+:\s+(?P<audt_sess_id>\S+)$')

        # Security Grp : none
        p23 = re.compile(r'^Security\s+Grp\s+:\s+(?P<security_group>\S+)$')

        # Public IP    : 10.229.20.77
        p24 = re.compile(r'^Public\s+IP\s+:\s+(?P<public_ip>\S+)$')

        # Encryption   : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)AES256
        # Encryption   : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)AES256  DTLS-Tunnel: (1)AES256
        p25 = re.compile(r'^Encryption\s+:\s+(?P<protocol>\S+):\s+(?P<encryption>\S+)'
                         r'\s+SSL-Tunnel:\s+(?P<ssl_tunnel>\S+)'
                         r'(\s+DTLS-Tunnel:\s+(?P<dtls_tunnel>\S+))?$')

        # Hashing      : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)SHA1
        # Hashing      : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)SHA1  DTLS-Tunnel: (1)SHA1
        p26 = re.compile(r'^Hashing\s+:\s+(?P<protocol>\S+):\s+(?P<hashing>\S+)'
                         r'\s+SSL-Tunnel:\s+(?P<ssl_tunnel>\S+)'
                         r'(\s+DTLS-Tunnel:\s+(?P<dtls_tunnel>\S+))?$')

        # -------------------------------------------------------------------
        # Regular expression for 'show vpn-sessiondb summary'-like output
        # -------------------------------------------------------------------

        # VPN Session Summary
        # Tunnels Summary
        p2_1 = re.compile(r'^(?P<summary_name>(VPN Session|Tunnels)) Summary$')

        # AnyConnect Client            :    127 :        432 :         205 :        0
        # Clientless VPN               :      0 :          1 :           1
        p2_2 = re.compile(r'^(?P<name>(AnyConnect Client|Clientless VPN)) +: +(?P<active>\d+) *'
                          r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                          r'( *: +(?P<inactive>\d+))?$')

        # SSL/TLS/DTLS               :    127 :        432 :         205 :        0
        # Browser                    :      0 :          1 :           1
        p2_3 = re.compile(r'^(?P<name>(SSL/TLS/DTLS|Browser)) +: +(?P<active>\d+) *'
                          r': +(?P<cumulative>\d+) *: +(?P<peak_concurrent>\d+)'
                          r'( *: +(?P<inactive>\d+))?$')

        # Total Active and Inactive    :    127             Total Cumulative :    432
        p2_4 = re.compile(r'^Total +Active +and +Inactive +: +'
                          r'(?P<total_active_and_inactive>\d+) +Total +Cumulative +: +'
                          r'(?P<total_cumulative>\d+)$')

        # AnyConnect-Parent            :    127 :        432 :             205
        # SSL-Tunnel                   :    125 :       1577 :             204
        # DTLS-Tunnel                  :    124 :       1508 :             202
        # Totals                       :    376 :       3517
        p2_5 = re.compile(r'^(?P<name>(Totals|DTLS-Tunnel|SSL-Tunnel|AnyConnect-Parent))'
                          r' +: +(?P<active>\d+) *: +(?P<cumulative>\d+)'
                          r'( *: +(?P<peak_concurrent>\d+))?( *: (?P<inactive>\d+))?$')

        # Device Total VPN Capacity    :   5000
        p2_6 = re.compile(r'^Device\s+Total\s+VPN\s+Capacity\s+:'
                          r'\s+(?P<device_total_vpn_capacity>\d+)$')

        # Device Load                  :     0%
        p2_7 = re.compile(r'^Device +Load +: +(?P<device_load>\d+)\%$')

        for line in output.splitlines():
            line = line.strip()

            # Session Type: SSL VPN Client
            m = p1.match(line)
            if m:
                session_type_dict = parsed_dict.setdefault('session_type', {}).\
                                                setdefault(m.groupdict()['session_type'], {})
                continue

            # Username : lee
            # Username : lee Index : 1
            m = p2.match(line)
            if m:
                group = m.groupdict()
                username_dict = session_type_dict.setdefault('username', {}).\
                                                  setdefault(group['username'], {})

                if group['index']:
                    index_dict = username_dict.setdefault('index', {}).\
                                                  setdefault(int(group['index']), {})
                continue

            # Index : 1 IP Addr : 192.168.16.232
            m = p3.match(line)
            if m:
                index_dict = username_dict.setdefault('index', {}).\
                                                  setdefault(int(m.groupdict()['index']), {})
                index_dict['ip_addr'] = m.groupdict()['ip_addr']
                continue

            # Protocol : SSL VPN Client Encryption : 3DES
            # Protocol : AnyConnect-Parent SSL-Tunnel DTLS-Tunnel
            m = p4.match(line)
            if m:
                index_dict['protocol'] = m.groupdict()['protocol']
                if m.groupdict()['vpn_client_encryption']:
                    index_dict['vpn_client_encryption'] = m.groupdict()['vpn_client_encryption']
                continue

            # Hashing : SHA1 Auth Mode : userPassword
            # Client Ver : Cisco STC 10.4.0.117
            # Client Type : Internet Explorer
            # Group : DfltGrpPolicy
            # Login Time : 14:32:03 UTC Wed Mar 20 2007
            # Duration : 0h:00m:04s
            # Inactivity : 0h:00m:04s
            # Filter Name :
            # License : AnyConnect Premium
            # NAC Result : Unknown
            # Audt Sess ID : 0adc27fd093260005381
            # Security Grp : none
            # Public IP    : 10.229.20.77
            # Assigned IP : 192.168.246.2 Public IP : 10.139.1.3
            # Encryption : RC4 AES128 Hashing : SHA1
            # Group Policy : EngPolicy Tunnel Group : EngGroup
            # Group Policy : GroupPolicy_Employee
            # Tunnel Group : Employee
            # VLAN Mapping : N/A VLAN : none
            m = p5.match(line) or p9.match(line) or \
                p10.match(line) or p11.match(line) or p12.match(line) or \
                p13.match(line) or p14.match(line) or p15.match(line) or \
                p17.match(line) or p20.match(line) or p22.match(line) or \
                p23.match(line) or p24.match(line) or p16.match(line) or \
                p18.match(line) or p19.match(line) or p21.match(line)

            if m:
                group = m.groupdict()

                for k in group.keys():
                    if group[k]:
                        index_dict[k] = group[k]

                continue

            # Hashing : AnyConnect-Parent: (1)none
            m = p5_1.match(line)
            if m:
                index_dict['hashing'] = m.groupdict()['hashing']
                continue

            # Encryption   : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)AES256
            # Encryption   : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)AES256  DTLS-Tunnel: (1)AES256
            m = p25.match(line)
            if m:
                group = m.groupdict()
                for k in ['encryption', 'ssl_tunnel', 'dtls_tunnel']:
                    if group[k]:
                        index_dict[k] = group[k]
                continue

            # Hashing      : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)SHA1
            # Hashing      : AnyConnect-Parent: (1)none  SSL-Tunnel: (1)SHA1  DTLS-Tunnel: (1)SHA1
            m = p26.match(line)
            if m:
                group = m.groupdict()
                for k in ['hashing', 'ssl_tunnel', 'dtls_tunnel']:
                    if group[k]:
                        index_dict[k] = group[k]
                continue

            # TCP Dst Port : 443 TCP Src Port : 54230
            m = p6.match(line)
            if m:
                tcp_dict = index_dict.setdefault('tcp', {})
                tcp_dict['src_port'] = int(m.groupdict()['src_port'])
                tcp_dict['dst_port'] = int(m.groupdict()['dst_port'])
                continue

            # Bytes Tx : 20178 Bytes Rx : 8662
            # Pkts Tx : 27 Pkts Rx : 19
            m = p7.match(line)
            if m:
                group = m.groupdict()
                txrx_dict = index_dict.setdefault(group['type'].lower(), {})
                txrx_dict['tx'] = int(group['tx'])
                txrx_dict['rx'] = int(group['rx'])
                continue

            # Encryption : AnyConnect-Parent: (1)none
            # Encryption   : Clientless: (1)AES128  Hashing      : Clientless: (1)SHA256
            m = p18_1.match(line)
            if m:
                group = m.groupdict()
                index_dict['encryption'] = group['encryption']
                if group['hashing']:
                    index_dict['hashing'] = group['hashing']
                continue

            # -------------------------------------------------------------------
            # Parse 'show vpn-sessiondb summary'-like output
            # -------------------------------------------------------------------

            # VPN Session Summary
            # Tunnels Summary
            m = p2_1.match(line)
            if m:
                summary_name = m.groupdict()['summary_name'].lower().replace(' ', '_')
                parsed_dict.setdefault('summary', {}).setdefault(summary_name, {})
                continue

            # AnyConnect Client            :    127 :        432 :         205 :        0
            # Clientless VPN               :      0 :          1 :           1
            m = p2_2.match(line)
            if m:
                group = m.groupdict()
                name = group['name'].lower().replace(' ', '_')
                if name not in parsed_dict['summary']['vpn_session']:
                    sub_dict = parsed_dict['summary']['vpn_session']\
                                                .setdefault(name, {})

                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    if group.get(k):
                        sub_dict[k] = int(group.get(k))
                continue

            # SSL/TLS/DTLS               :    127 :        432 :         205 :        0
            # Browser                    :      0 :          1 :           1
            m = p2_3.match(line)
            if m:
                group = m.groupdict()
                name = group['name'].lower().replace('/', '_')
                sub_dict_2 = sub_dict.setdefault(name, {})
                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    if group.get(k):
                        sub_dict_2[k] = int(group.get(k))
                continue

            # Total Active and Inactive    :    127             Total Cumulative :    432
            # Device Total VPN Capacity    :   5000
            m = p2_4.match(line) or p2_6.match(line)
            if m:
                group = m.groupdict()
                for k in ['total_active_and_inactive', 'total_cumulative', 'device_total_vpn_capacity']:
                    if group.get(k):
                        parsed_dict['summary']['vpn_session'][k] = int(group.get(k))
                continue

            # AnyConnect-Parent            :    127 :        432 :             205
            # SSL-Tunnel                   :    125 :       1577 :             204
            # DTLS-Tunnel                  :    124 :       1508 :             202
            # Totals                       :    376 :       3517
            m = p2_5.match(line)
            if m:
                group = m.groupdict()
                name = group['name'].lower().replace('-', '_')
                tunnels_sub_dict = parsed_dict['summary']['tunnels'].setdefault(name, {})
                for k in ['active', 'cumulative', 'peak_concurrent', 'inactive']:
                    if group[k]:
                        tunnels_sub_dict[k] = int(group[k])
                continue

            # Device Load                  :     0%
            m = p2_7.match(line)
            if m:
                group = m.groupdict()
                k = 'device_load'
                device_load = int(group[k])/100
                parsed_dict['summary']['vpn_session'][k] = device_load
                continue

        return parsed_dict


# =============================================
# Parser for
#         * show vpn-sessiondb
# =============================================
class ShowVpnSessiondb(ShowVpnSessiondbSuper, ShowVpnSessiondbSchema):
    """Parser for
        * show vpn-sessiondb
    """
    cli_command = 'show vpn-sessiondb'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        return super().cli(output=out)


# =============================================
# Parser for
#         * show vpn-sessiondb anyconnect
#         * show vpn-sessiondb anyconnect sort inactivity
# =============================================
class ShowVpnSessiondbAnyconnect(ShowVpnSessiondbSuper, ShowVpnSessiondbSchema):
    """Parser for
        * show vpn-sessiondb anyconnect
        * show vpn-sessiondb anyconnect {sort} inactivity
    """
    cli_command = ['show vpn-sessiondb anyconnect',
                   'show vpn-sessiondb anyconnect {sort} inactivity']

    def cli(self, sort='', output=None):
        if output is None:
            if sort:
                cmd = self.cli_command[1].format(sort=sort)
            else:
                cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output

        return super().cli(output=out, sort=sort)


# =============================================
# Parser for
#         * show vpn-sessiondb webvpn
# =============================================
class ShowVpnSessiondbWebvpn(ShowVpnSessiondbSuper, ShowVpnSessiondbSchema):
    """Parser for
        * show vpn-sessiondb webvpn
    """
    cli_command = 'show vpn-sessiondb webvpn'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        return super().cli(output=out)
