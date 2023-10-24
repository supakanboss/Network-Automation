from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def auto_config_vlan(filtered_nr):
    
    num_vlans = int(input("How many VLANs do you want to create : "))

    total_interfaces = 20
    interfaces_per_vlan = total_interfaces // num_vlans

    base_vlan_id = 100
    vlans = [base_vlan_id + (i * 100) for i in range(num_vlans)]

    config_commands = ["enable"]

    for vlan in vlans:
        config_commands += [
            "conf t",
            f"vlan {vlan}",
            "exit"
        ]

    current_interface = 1

    for i, vlan in enumerate(vlans):
        for _ in range(interfaces_per_vlan):
            config_commands += [
                f"interface g1/0/{current_interface}",
                "switchport mode access",
                f"switchport access vlan {vlan}"
            ]
            print(f"Assigned fa g1/0/{current_interface} to VLAN {vlan}")
            current_interface += 1

    config_str = "\n".join(config_commands)
    result = filtered_nr.run(task=send_command, command=config_str)
    print_result(result)
    filtered_nr.close_connections()