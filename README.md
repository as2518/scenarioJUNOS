# scenarioJUNOS
Scenario based Network Operation Tool for JUNOS router using PyEZ/JSNAPy.

System
![system_en](https://cloud.githubusercontent.com/assets/7057797/21740336/53a2cffa-d4fa-11e6-8971-f6627333a14e.png)

# How to run

```
python run_scenario.py -f <scenario file>
```

#Scenario file sample

```yaml:scenario_demo.yml
purpus:  |
  This operation target is BGP private peering
  with ABC company(AS65002).
operator: Taiji Tsuchiya
operation_date: 20161115
hosts:
  management_ipaddress: 192.168.34.16
  hostname: firefly1
  model: firefly-perimeter
  username: user1
  password: password1
scenario:
  - test_hostname
  - test_model
  - test_interface:
      interface_name: ge-0/0/2
      interface_status: up
  - set_add_interface:
      interface_name: ge-0/0/2
      interface_address_ipv4: 192.168.35.1
      interface_subnet_ipv4: 30
      interface_description: AS65002_peer
  - test_interface:
      interface_name: ge-0/0/2
      interface_status: up
  - set_add_bgp_neighbor:
      interface_name: ge-0/0/2
      neighbor_asnum: 65002
      local_asnum: 65001
      neighbor_address_ipv4: 192.168.35.2
      neighbor_description: AS65002_peer
  - test_bgp_neighbor:
      neighbor_address_ipv4: 192.168.35.2
      neighbor_status: Established
  - set_add_bgp_policy_external:
      external_policy_name: AS65002_export
      advertised_route_address_ipv4: 10.10.10.0
      advertised_route_subnet_ipv4: 24
      interface_name: ge-0/0/2
      neighbor_address_ipv4: 192.168.35.2
  - sleep_10sec
  - test_bgp_received_route:
      neighbor_address_ipv4: 192.168.35.2
      received_route_address_ipv4: 10.10.30.0
      received_route_subnet_ipv4: 24
  - test_bgp_advertised_route:
      neighbor_address_ipv4: 192.168.35.2
      advertised_route_address_ipv4: 10.10.10.0
      advertised_route_subnet_ipv4: 24
```

# Template sample

router set templamte is put on './set_templates' directory.

```yaml:./set_templates/add_interface.jinja2
interfaces {
   {{ interface_name }} {
        unit 0 {            
            description {{ interface_description }};
            family inet {
                address {{ interface_address_ipv4 }}/{{ interface_subnet_ipv4 }};
            }
        }
    }
}
```

router test template is put on './test_templates' directory.

```yaml:./test_templates/test_interface.jinja2
test_interface_{{ interface_name }}_{{ interface_status }}:
  - command: show interfaces terse {{ interface_name }}
  - item:
      xpath: physical-interface
      tests:
        - is-equal: admin-status, {{ interface_status }}
        - is-equal: oper-status, {{ interface_status }}
```


# Output Sample
demo: configuring interface and BGP neighbor setting
- Left : scenarioJUNOS tool
- Right top : target JUNOS router(hostname: firefly1)
- Right bottom : BGP neighbor router, not target (hostname: firefly2)

![demo](https://qiita-image-store.s3.amazonaws.com/0/45596/c29b2bca-e4e0-aab9-58c7-f2e382ceea2f.gif)

green: OK statement
red: NG statement
yellow: User determination statement (example: commit or discard)
![Screen Shot 2016-12-02 at 8.21.18 AM.png](https://qiita-image-store.s3.amazonaws.com/0/45596/bb6b4404-ea84-128a-c6d5-4575ce44a2a1.png)
![Screen Shot 2016-12-02 at 8.21.35 AM.png](https://qiita-image-store.s3.amazonaws.com/0/45596/a19f75c3-b707-50d0-7ea7-a1cdb682d98f.png)
![Screen Shot 2016-12-02 at 8.22.03 AM.png](https://qiita-image-store.s3.amazonaws.com/0/45596/0429eebd-9d78-8544-e7b6-f860eb9f43ed.png)
![Screen Shot 2016-12-02 at 8.22.25 AM.png](https://qiita-image-store.s3.amazonaws.com/0/45596/80e71156-02d4-e807-0a9c-fe9bf3781747.png)
![Screen Shot 2016-12-02 at 8.22.37 AM.png](https://qiita-image-store.s3.amazonaws.com/0/45596/7a852322-a2ef-5d22-85dc-fbbc107a31a0.png)
