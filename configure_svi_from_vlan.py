import re
from connection_command import send_command_host


def configure_svi_from_vlan(filtered_nr):
    
    base_ip = input("Enter the base IP address for SVI (e.g., 192.168.x.254): ")

    base_parts = base_ip.split(".")
    if len(base_parts) != 4 or 'x' not in base_parts:
        print("Invalid IP address format.")
        return

    base_third_octet = 10

    for host in filtered_nr.inventory.hosts.values():
        
        vlans_output = send_command_host(host, "show vlan brief")
        
        # Match VLAN lines where the name starts with "VLAN"
        vlan_pattern = re.compile(r"^(\d+)\s+VLAN", re.MULTILINE)
        vlan_ids = vlan_pattern.findall(vlans_output)

        if not vlan_ids:
            print(f"No VLANs with the name starting with 'VLAN' found on {host.name}. Terminating.")
            return

        for vlan_id in vlan_ids:
            svi_third_octet = base_third_octet + int(vlan_id) // 100 * 10
            
            svi_ip = f"{base_parts[0]}.{base_parts[1]}.{svi_third_octet}.{base_parts[3]}"
            
            config = f"""
            enable
            conf t
            interface Vlan{vlan_id}
            ip address {svi_ip} 255.255.255.0
            end
            """
            
            result = send_command_host(host, config)
            
            if "error" not in result.lower() and "invalid" not in result.lower():
                print(f"Configured SVI for VLAN {vlan_id} on {host.name} with IP {svi_ip}")
            else:
                print(f"An error occurred while configuring SVI for VLAN {vlan_id} on {host.name}: {result}")