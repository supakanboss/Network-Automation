from connection_command import send_command_host

def auto_generate_ip(filtered_nr):
    
    third_octet_increment = 10
    
    base_ip = input("Enter the base IP address (e.g., 192.168.x.1): ")
    interface_choice = input("Choose interface (inside/outside): ")
    
    base_parts = base_ip.split(".")
    
    if not (len(base_parts) == 4 and (base_parts[2] == 'x' or (0 <= int(base_parts[2]) < 256))):
        print("Invalid IP address provided.")
        return

    base_third_octet = 10 if base_parts[2] == 'x' else int(base_parts[2])  
    
    interface_map = {
        "inside": "interface g0/0/0",
        "outside": "interface g0/0/1"
    }
    
    interface = interface_map.get(interface_choice)
    if not interface:
        print("Invalid interface choice.")
        return

    for host in filtered_nr.inventory.hosts.values():
        new_ip = ".".join(base_parts[:2] + [str(base_third_octet)] + [base_parts[3]])
        
        config = f"""
        enable
        conf t
        {interface}
        no shutdown
        ip address {new_ip} 255.255.255.0
        end
        """
        
        result = send_command_host(host, config)
        if "error" not in result.lower() and "invalid" not in result.lower():
            print(f"Configured {host} with IP {new_ip} on {interface_choice} interface.")
        else:
            print(f"An error occurred while configuring {host}: {result}")
        base_third_octet += third_octet_increment