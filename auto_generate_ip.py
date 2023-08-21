from connection_command import send_command_host

def auto_generate_ip(filtered_nr):
    
    third_octet_increment = 10
    
    base_ip = input("Enter the base IP address (e.g., 192.168.x.1): ")
    interface_choice = input("Choose interface (inside/outside): ")
    
    base_parts = base_ip.split(".")
    
    if len(base_parts) != 4 or 'x' not in base_ip:
        print("Invalid IP address provided.")
        return

    x_position = base_parts.index('x')  
    base_parts[x_position] = '10'  

    interface_map = {
        "inside": "interface g0/0/0",
        "outside": "interface g0/0/1"
    }
    
    interface = interface_map.get(interface_choice)
    if not interface:
        print("Invalid interface choice.")
        return

    for host in filtered_nr.inventory.hosts.values():
        new_ip = ".".join(base_parts)
        
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

        # Increment the value in the position where 'x' was
        base_parts[x_position] = str(int(base_parts[x_position]) + third_octet_increment)
