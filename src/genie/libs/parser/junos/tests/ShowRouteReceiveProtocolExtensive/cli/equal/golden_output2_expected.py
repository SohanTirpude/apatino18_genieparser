expected_output = {
    "route-information": {
        "route-table": [
            {
                "active-route-count": "18",
                "destination-count": "18",
                "hidden-route-count": "0",
                "holddown-route-count": "0",
                "rt": {
                    "rt-announced-count": "2",
                    "rt-destination": "2001:db8:100::",
                    "rt-entry": {
                        "as-path": "AS path: I",
                        "bgp-path-attributes": {
                            "attr-as-path-effective": {
                                "aspath-effective-string": "AS path:",
                                "attr-value": "I",
                            }
                        },
                        "bgp-rt-flag": "Accepted",
                        "local-preference": "100",
                        "nh": {"to": "2001:db8:100::1"},
                    },
                    "rt-entry-count": {"#text": "3"},
                    "rt-prefix-length": "48",
                },
                "table-name": "inet6.0",
                "total-route-count": "22",
            },
            {
                "active-route-count": "3",
                "destination-count": "3",
                "hidden-route-count": "0",
                "holddown-route-count": "0",
                "table-name": "inet6.3",
                "total-route-count": "3",
            },
        ]
    }
}
