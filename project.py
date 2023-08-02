from netmiko import ConnectHandler
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from getpass import getpass
from netmiko import ConnectHandler

def send_command(task, command):
    
    device_name = task.host.name
    password = passwords[device_name]  
    device_type = task.host.get('device_type', 'cisco_ios_telnet')  
    
    net_connect = ConnectHandler(device_type=device_type, ip=task.host.hostname, username=task.host.username, password=password)
    
    result = net_connect.send_command_timing("enable")  
    if "Password:" in result:  
        result += net_connect.send_command_timing(password)  
    
    result += net_connect.send_command_timing(command)  
    net_connect.disconnect()

    return {
        "output": result,
    }

def filter_group(nr, group_name):
    
    filtered_nr = nr.filter(F(groups__contains=group_name))
    hosts = filtered_nr.inventory.hosts
    num_hosts = len(hosts)
    
    if num_hosts > 0:
        print(f"Number of hosts after filtering: {num_hosts}")
        print("Devices in group '{}':".format(group_name))
        return filtered_nr, hosts
    else:
        print("No devices found in group '{}'.".format(group_name))
        return None, None

def show_data(filtered_nr):
    
    show_interfaces_command = "enable\nshow interface"
    
    result = filtered_nr.run(task=send_command, command=show_interfaces_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ipv4(filtered_nr):
        
    interface = input("Enter the Interface (ex. f1/1): ")
    network_address = input("Enter the IPv4 address: ")
    subnet = input("Enter the Subnet mask: ")
    set_ipv4_command = "enable\nconf t\n"  
    
    set_ipv4_command += "ip routing\n"
    set_ipv4_command += f"interface {interface}\n"
    set_ipv4_command += "no shutdown\n"
    set_ipv4_command += "no switchport\n"
    set_ipv4_command += f"ip address {network_address} {subnet}\n"
    
    result = filtered_nr.run(task=send_command, command=set_ipv4_command)
    print_result(result)
    filtered_nr.close_connections()

def set_vlan(filtered_nr, group_name):
    
    print("******************** "+"---- Device Group : "+ group_name +" -----\n")
    print("1 - Set VLAN")
    print("2 - Set Trunk")
    print("3 - Set Native VLAN")
    print("4 - Set IPv4 Address in VLAN")
    print("5 - Back\n")
    print("********************")
    action = input("Choose action: ")
    set_vlan_command = "enable\nconf t\n"  
    
    if action == "1":
        vlan_num = input("Enter the VLAN Number: ")
        vlan_name = input("Enter the VLAN Name: ")
        interface = input("Enter the Interface (ex. f1/1-12): ")
        
        set_vlan_command += f"vlan {vlan_num}\n"
        set_vlan_command += f"name {vlan_name}\n"
        set_vlan_command += f"ex\n"
        set_vlan_command += f"interface range {interface}\n"
        set_vlan_command += f"switch mode access\n"
        set_vlan_command += f"switch access vlan {vlan_num}\n"
    
    elif action == "2":
        vlan_num = input("Enter the VLAN Number: ")
        interface = input("Enter the Interface (ex. f1/1): ")
        
        set_vlan_command += f"interface {interface}\n"
        set_vlan_command += f"switch mode trunk\n"
        set_vlan_command += f"switch trunk allowed vlan {vlan_num}\n"
    
    elif action == "3":
        vlan_num = input("Enter the Native VLAN Number: ")
        interface = input("Enter the Trunk Interface (ex. f1/1): ")   
        
        set_vlan_command += f"interface {interface}\n"
        set_vlan_command += f"switch trunk native vlan {vlan_num}\n"
    
    elif action == "4":
        vlan_num = input("Enter the VLAN Number: ")
        network_address = input("Enter the IPv4 address: ")
        subnet = input("Enter the Subnet mask: ")
        
        set_vlan_command += f"interface vlan {vlan_num}\n"
        set_vlan_command += f"ip address {network_address} {subnet}\n"
    
    elif action == "5":
        return
    
    result = filtered_nr.run(task=send_command, command=set_vlan_command)
    print_result(result) 
    filtered_nr.close_connections()

def set_ether_channel(filtered_nr):
    
    interface = input("Enter the Interface (ex. f1/1-12): ")
    channel_group_number = input("Enter the Channel group number: ")
    vlan_number = input("Enter the VLAN Number: ")
    
    set_ether_channel_command = "enable\nconf t\n"
    
    set_ether_channel_command += f"interface range {interface}\n"
    set_ether_channel_command += f"channel-group {channel_group_number} mode active\n"
    set_ether_channel_command += f"ex\n"
    set_ether_channel_command += f"interface port-channle {channel_group_number}\n"
    set_ether_channel_command += f"switch mode trunk\n"
    set_ether_channel_command += f"switch trunk allowed vlan {vlan_number}\n"
    
    result = filtered_nr.run(task=send_command, command=set_ether_channel_command)
    print_result(result)
    filtered_nr.close_connections()

def set_static_routing(filtered_nr):
    
    network_address = input("Enter the Network address: ")
    subnet = input("Enter the Subnet mask: ")
    next_hop = input("Enter the Next hop: ")
    
    routing_command = "enable\nconf t\n"
    routing_command += f"ip route {network_address} {subnet} {next_hop}\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_dynamic_routing(filtered_nr, group_name):
    
    print("******************** "+"---- Device Group : "+ group_name +" -----\n")
    print("1 - Set Router ID")
    print("2 - Set OSPF")
    print("3 - Set Virtual Link")
    print("4 - Set EIGRP")
    print("5 - Set Redistribute")
    print("6 - Clear OSPF process")
    print("7 - Back\n")
    print("********************")
    action = input("Choose action : ")
    routing_command = "enable\nconf t\n"
    
    if action == "1":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        
        routing_command += f"router ospf {router_ospf_process}\n"
        routing_command += f"router-id {router_id}\n"
    
    elif action == "2":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        network_address = input("Enter the Network address (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        ospf_area = input("Enter the OSPF area: ")
        
        routing_command += f"router ospf {router_ospf_process}\n"
        
        for network_address, wildcard_mask in zip(network_address, wildcard_masks):
            routing_command += f"network {network_address.strip()} {wildcard_mask.strip()} area {ospf_area}\n"
    
    elif action == "3":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        ospf_area = input("Enter the OSPF area: ")
        router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        
        routing_command += f"router ospf {router_ospf_process}\n"
        routing_command += f"area {ospf_area} virtual-link {router_id}\n"
    
    elif action == "4":
        
        network_address = input("Enter the Network address (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        
        routing_command += "router eigrp 1\n"
        
        for network_address, wildcard_mask in zip(network_address, wildcard_masks):
            routing_command += f"network {network_address.strip()} {wildcard_mask.strip()}\n"
    
    elif action == "5":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        router_eigrp_process = input("Enter the Router EIGRP process number: ")
        
        routing_command += f"router ospf {router_ospf_process}\n"
        routing_command += f"redistribute eigrp {router_eigrp_process} subnets\n"
        routing_command += f"router eigrp {router_eigrp_process}\n"
        routing_command += f"redistribute ospf {router_eigrp_process} metric 1000 10 255 1 1500\n"
    
    elif action == "6":
    
        routing_command += f"do clear ip ospf process\n"
        routing_command += f"yes\n"
    
    elif action == "7":
        return
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_dhcp(filtered_nr, group_name):
    
    print("******************** "+"---- Device Group : "+ group_name +" -----\n")
    print("1 - Set DHCP Pool")
    print("2 - Set Excluded IP Address")
    print("3 - Optional Default Router")
    print("4 - Optional DNS Server")
    print("5 - Optional Set the lease duration for clients in minutes")
    print("6 - Back\n")
    print("********************")
    action = input("Choose action : ")
    dhcp_command = "enable\nconf t\n"
    
    if action == "1":
        dhcp_pool_name = input("Enter the DHCP Pool Name: ")
        network_address = input("Enter the Network Address: ")
        subnet = input("Enter the Subnet mask: ")
        
        dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
        dhcp_command += f"network {network_address} {subnet}\n"
    
    elif action == "2":
        network_address = input("Enter the Network Address (comma-separated): ").split(',')
        
        for network_address in zip(network_address):
            dhcp_command += f"ip dhcp excluded-address {network_address.strip()}\n"
    
    if action == "3":
        dhcp_pool_name = input("Enter the DHCP Pool Name: ")
        default_router_ip_address = input("Enter the Default Gateway IP Address: ")
        
        dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
        dhcp_command += f"default-router {default_router_ip_address}\n"
    
    if action == "4":
        dhcp_pool_name = input("Enter the DHCP Pool Name: ")
        dns_server_ip_address = input("Enter the DNS Server IP Address: ")
        
        dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
        dhcp_command += f"dns-server {dns_server_ip_address}\n"
    
    if action == "5":
        dhcp_pool_name = input("Enter the DHCP Pool Name: ")
        lease_duration_minutes = input("Enter the Lease Duration Minutes: ")
        
        dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
        dhcp_command += f"lease {lease_duration_minutes}\n"
    
    if action == "6":
        return
    
    result = filtered_nr.run(task=send_command, command=dhcp_command)
    print_result(result)
    filtered_nr.close_connections()

def set_nat_pat(filtered_nr, group_name):
    
    print("******************** "+"---- Device Group : "+ group_name +" -----\n")
    print("1 - Set NAT Static")
    print("2 - Set PAT 1 Public ip address")
    print("3 - Set PAT more than 1 Public ip address")
    print("4 - Set Out side")
    print("5 - Set In side")
    print("6 - Back\n")
    print("********************")
    action = input("Choose action : ")
    set_nat_pat_command = "enable\nconf t\n"
    
    if action == "1":
        
        private_ip_address = input("Enter the Private ip address (comma-separated): ").split(',')
        public_ip_address = input("Enter the Public ip address (comma-separated): ").split(',')
        
        for private_ip_address, public_ip_address in zip(private_ip_address, public_ip_address):
            set_nat_pat_command += f"ip nat inside source static {private_ip_address.strip()} {public_ip_address.strip()}\n"
    
    elif action == "2":
        
        ip_access_list_name = input("Enter the IP access list Standard name: ")
        network_address = input("Enter the Network address (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        interface = input("Enter the Out side interface (ex. f1/1): ")
        
        set_nat_pat_command += f"ip access-list standard {ip_access_list_name}\n"
        
        for network_address, wildcard_mask in zip(network_address, wildcard_masks):
            set_nat_pat_command += f"permit {network_address.strip()} {wildcard_mask.strip()}\n"
        
        set_nat_pat_command += f"ex\n"
        set_nat_pat_command += f"ip nat inside source list {ip_access_list_name} interface {interface} overload\n"
    
    elif action == "3":
        
        ip_access_list_name = input("Enter the IP access list Standard name: ")
        network_address = input("Enter the Network address (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        ip_nat_pool_name = input("Enter the IP NAT pool name: ")
        public_ip_address_start = input("Enter the Public ip address (Start): ")
        public_ip_address_end = input("Enter the Public ip address (End): ")
        netmask_public_ip = input("Enter the Netmask Public ip address : ")
        
        set_nat_pat_command += f"ip access-list standard {ip_access_list_name}\n"
        
        for network_address, wildcard_mask in zip(network_address, wildcard_masks):
            set_nat_pat_command += f"permit {network_address.strip()} {wildcard_mask.strip()}\n"
        
        set_nat_pat_command += f"ex\n"
        set_nat_pat_command += f"ip nat pool {ip_nat_pool_name} {public_ip_address_start} {public_ip_address_end} netmask {netmask_public_ip}\n"
        set_nat_pat_command += f"ip nat inside source list {ip_access_list_name} pool {ip_nat_pool_name} overload\n"
    
    elif action == "4":
        interface = input("Enter the NAT Out-side Interface (ex. f1/1): ")
        set_nat_pat_command += f"interface {interface}\n"
        set_nat_pat_command += f"ip nat outside\n"
    
    elif action == "5":
        interface = input("Enter the NAT In-side Interface (ex. f1/1): ")
        set_nat_pat_command += f"interface {interface}\n"
        set_nat_pat_command += f"ip nat inside\n"
    
    elif action == "6":
        return
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def ipv6(filtered_nr, group_name):
    
    print("******************** "+"---- Device Group : "+ group_name +" -----\n")
    print("1 - Set IPv6 Address in Interface")
    print("2 - Set IPv6 Address in VLAN")
    print("3 - Set IPv6 EUI-64")
    print("4 - Set Tunnel IPv4/IPv6\n")
    print("OSPFv3 Dynamic Routing\n")
    print("5 - Set Router ID")
    print("6 - Set OSPFv3")
    print("7 - Clear IPv6 OSPF Process")
    print("8 - Back\n")
    print("********************")
    action = input("Choose action : ")
    ipv6_command = "enable\nconf t\n"
    
    if action == "1":
        
        interface = input("Enter the Interface (ex. f1/1): ")
        address = input("Enter the IPv6 address: ")
        prefix_lengths = input("Enter the Prefix Lengths: ")
    
        ipv6_command += f"ipv6 unicast-routing\n"
        ipv6_command += f"interface {interface}\n"
        ipv6_command += f"no shutdown\n"
        ipv6_command += f"no switchport\n"
        ipv6_command += f"ipv6 address {address}/{prefix_lengths}\n"

    elif action == "2":
        
        vlan_number = input("Enter the VLAN Nmuber: ")
        address = input("Enter the IPv6 address: ")
        prefix_lengths = input("Enter the Prefix Lengths: ")
    
        ipv6_command += f"ipv6 unicast-routing\n"
        ipv6_command += f"interface vlan {vlan_number}\n"
        ipv6_command += f"ipv6 address {address}/{prefix_lengths}\n"
    
    elif action == "3":
        
        interface = input("Enter the Interface (ex. f1/1 or vlan 10): ")
        address = input("Enter the IPv6 address: ")
        prefix_lengths = input("Enter the Prefix Lengths: ")
    
        ipv6_command += f"ipv6 unicast-routing\n"
        ipv6_command += f"interface {interface}\n"
        ipv6_command += f"ipv6 address {address}/{prefix_lengths} eui-64\n"

    elif action == "4":
        
        tunnel_number = input("Enter the Interface Tunnel Number: ")
        address = input("Enter the IPv6 address: ")
        prefix_lengths = input("Enter the Prefix Lengths: ")
        tunnel_source = input("Enter the Tunnel Source (ex. g0/0/0): ")
        tunnel_destination = input("Enter the Tunnel Destination (IPv4 Address): ")
        
        ipv6_command += f"interface tunnel {tunnel_number}\n"
        ipv6_command += f"ipv6 address {address}/{prefix_lengths}\n"
        ipv6_command += f"tunnel source {tunnel_source}\n"
        ipv6_command += f"tunnel destination {tunnel_destination}\n"
        ipv6_command += f"tunnel tunnel mode ipv6ip\n"
    
    elif action == "5":
        
        ospfv3_process_number = input("Enter the Router OSPFv3 process number: ")
        router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        
        ipv6_command += f"ipv6 router ospf {ospfv3_process_number}\n"
        ipv6_command += f"router-id {router_id}\n"
    
    elif action == "6":
        
        ospfv3_process_number = input("Enter the Router OSPFv3 process number: ")
        interface = input("Enter the Interface (ex. f1/1-10,f1/14): ")
        ospfv3_area = input("Enter the OSPFv3 area: ")
        
        ipv6_command += f"interface {interface}\n"
        ipv6_command += f"ipv6 ospf {ospfv3_process_number} area {ospfv3_area}\n"
        
    elif action == "7":
        
        ipv6_command += f"do clear ipv6 ospf process\n"
        ipv6_command += f"yes\n"
        
    elif action == "8":
        return
        
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def backup_config(filtered_nr):
    
    print("Starting config backup...")
    command = "show running-config"

    for host in filtered_nr.inventory.hosts.values():
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params = netmiko_params.dict()  

        netmiko_params.pop("extras", None)  
        netmiko_params["host"] = netmiko_params.pop("hostname", None)  
        netmiko_params.pop("platform", None)  
        netmiko_params["device_type"] = host.platform

        enable_password = getpass(f"Enter enable password for {host}: ")
        netmiko_params["secret"] = enable_password

        try:
            with ConnectHandler(**netmiko_params) as conn:
                conn.enable()  
                output = conn.send_command(command)
                with open(f"backup/{host}.conf", "w") as file:
                    file.write(output)
                    print(f"Config for {host} saved!")
        except Exception as e:
            print(f"An error occurred while backing up {host}: {e}")

    print("Config backup complete.")

def restore_config(filtered_nr):
    
    print("Starting config restore...")

    for host in filtered_nr.inventory.hosts.values():
        config_file = f"backup/{host}.conf"  
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params = netmiko_params.dict()  

        netmiko_params.pop("extras", None)  
        netmiko_params["host"] = netmiko_params.pop("hostname", None)  
        netmiko_params.pop("platform", None)  

        enable_password = getpass(f"Enter enable password for {host}: ")
        netmiko_params["secret"] = enable_password
        netmiko_params["device_type"] = host.platform

        try:
            with ConnectHandler(**netmiko_params) as conn:
                conn.enable()  
                output = conn.send_config_from_file(config_file)
                print(f"Config for {host} restored!")
        except Exception as e:
            print(f"An error occurred while restoring config for {host}: {e}")

    print("Config restore complete.")

def main():
    
    global passwords  # Declare 'passwords' as a global variable
    nr = InitNornir(config_file="config.yaml")
    
    group_name = input("Enter the device group name: ")
    filtered_nr, hosts = filter_group(nr, group_name)
    
    if filtered_nr is None:
        return  # Exit the program if no devices are found in the specified group
    
    passwords = {}  # Initialize the 'passwords' dictionary here
    
    for host in hosts:
        password = getpass("Enter the password for device '{}': ".format(host))
        passwords[host] = password
    
    while True:
        
        print("******************** "+"---- Device Group : "+ group_name +" -----\n")
        print("1 - Show Data")
        print("2 - Set IPv4 Address")
        print("3 - Set VLAN")
        print("4 - Set Ether Channel")
        print("5 - Set Static  Routing")
        print("6 - Set Dynamic Routing")
        print("7 - Set DHCP")
        print("8 - Set NAT/PAT")
        print("9 - IPv6")
        print("10 - Change Device Group")
        print("11 - Backup Config")
        print("12 - Restore Config")
        print("13 - Exit\n")
        print("********************")  
        
        user_action = input("Choose action : ")
        
        if user_action == "1":
            show_data(filtered_nr)
        
        elif user_action == "2":
            set_ipv4(filtered_nr)
        
        elif user_action == "3":
            set_vlan(filtered_nr, group_name)
        
        elif user_action == "4":
            set_ether_channel(filtered_nr)
        
        elif user_action == "5":
            set_static_routing(filtered_nr)
        
        elif user_action == "6":
            set_dynamic_routing(filtered_nr, group_name)
        
        elif user_action == "7":
            set_dhcp(filtered_nr, group_name)
        
        elif user_action == "8":
            set_nat_pat(filtered_nr, group_name)
        
        elif user_action == "9":
            ipv6(filtered_nr, group_name)
        
        elif user_action == "10":
            group_name = input("Enter the device group name: ")
            filtered_nr, hosts = filter_group(nr, group_name)

            if filtered_nr is not None:
                passwords = {}  # Clear the 'passwords' dictionary
                for host in hosts:
                    password = getpass("Enter the password for device '{}': ".format(host))
                    passwords[host] = password
        
        elif user_action == "11":
            backup_config(filtered_nr)
        
        elif user_action == "12":
            restore_config(filtered_nr)
        
        elif user_action == "13":
            print("Exiting program...")
            break
        
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()