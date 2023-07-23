from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F
from getpass import getpass

def send_command(task, command):
    result = task.run(task=netmiko_send_command, command_string=command, use_timing=True)
    return {
        "output": result,
    }

def filter_group(nr):
    group_name = input("Enter the device group name: ")
    filtered_nr = nr.filter(F(groups__contains=group_name))
    print(f"Number of hosts after filtering: {len(filtered_nr.inventory.hosts)}")
    return filtered_nr

def show_data(filtered_nr, password):
    
    show_interfaces_command = f"enable\n{password}\nshow int"
    
    result = filtered_nr.run(task=send_command, command=show_interfaces_command)
    print_result(result)
    filtered_nr.close_connections()

def set_vlan(filtered_nr, password):
    print("********************\n")
    print("1 - Set VLAN\n")
    print("2 - Set Trunk\n")
    print("3 - Set Native VLAN\n")
    print("4 - Set Inter VLAN Routing\n")
    print("5 - Back\n")
    print("********************")
    action = input("Choose action: ")
    set_vlan_command = f"enable\n{password}\nconf t\n"
    
    if action == "1":
        vlan_num = input("Enter the VLAN Number: ")
        vlan_name = input("Enter the VLAN Name: ")
        interface = input("Enter the Interface (ex. f1/1-12): ")
        
        set_vlan_command += f"vlan {vlan_num}\n"
        set_vlan_command += f"name {vlan_name}\n"
        set_vlan_command += f"ex\n"
        set_vlan_command += f"int ra {interface}\n"
        set_vlan_command += f"sw mode acc\n"
        set_vlan_command += f"sw acc vlan {vlan_num}\n"
    
    elif action == "2":
        vlan_num = input("Enter the VLAN Number: ")
        interface = input("Enter the Interface (ex. f1/1): ")
        
        set_vlan_command += f"int {interface}\n"
        set_vlan_command += f"sw mode trunk\n"
        set_vlan_command += f"sw trunk allowed vlan {vlan_num}\n"
    
    elif action == "3":
        vlan_num = input("Enter the Native VLAN Number: ")
        interface = input("Enter the Trunk Interface (ex. f1/1): ")   
        
        set_vlan_command += f"int {interface}\n"
        set_vlan_command += f"sw trunk native vlan {vlan_num}\n"
    
    elif action == "4":
        vlan_num = input("Enter the VLAN Number: ")
        network_addresses = input("Enter the IP address: ")
        subnet = input("Enter the Subnet mask: ")
        
        set_vlan_command += f"int vlan {vlan_num}\n"
        set_vlan_command += f"ip add {network_addresses} {subnet}\n"
    
    elif action == "5":
        return
    
    result = filtered_nr.run(task=send_command, command=set_vlan_command)
    print_result(result) 
    filtered_nr.close_connections()

def set_ether_channel(filtered_nr, password):
    
    interface = input("Enter the Interface (ex. f1/1-12): ")
    channel_group_number = input("Enter the Channel group number: ")
    vlan_num = input("Enter the VLAN Number: ")
    set_ether_channel_command = f"enable\n{password}\nconf t\n"
    
    set_ether_channel_command += f"int ra {interface}\n"
    set_ether_channel_command += f"channel-group {channel_group_number} mode active\n"
    set_ether_channel_command += f"ex\n"
    set_ether_channel_command += f"int port-channle {channel_group_number}\n"
    set_ether_channel_command += f"sw mode trunk\n"
    set_ether_channel_command += f"sw trunk allowed vlan {vlan_num}\n"
    
    result = filtered_nr.run(task=send_command, command=set_ether_channel_command)
    print_result(result)
    filtered_nr.close_connections()

def set_static_routing(filtered_nr, password):
    
    network_addresses = input("Enter the Network addresses: ")
    subnet = input("Enter the Subnet mask: ")
    next_hop = input("Enter the Next hop: ")
    routing_command = f"enable\n{password}\nconf t\n"
    routing_command += f"ip route {network_addresses} {subnet} {next_hop}\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_dynamic_routing(filtered_nr, password):

    print("********************\n")
    print("1 - Set Router ID\n")
    print("2 - Set OSPF\n")
    print("3 - Set Virtual Link\n")
    print("4 - Set EIGRP\n")
    print("5 - Set Redistribute\n")
    print("6 - Clear OSPF process\n")
    print("7 - Back\n")
    print("********************")
    action = input("Choose action : ")
    routing_command = f"enable\n{password}\nconf t\n"
    
    if action == "1":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        routing_command += f"router ospf {router_ospf_process}\n"
        routing_command += f"router-id {router_id}\n"
    
    elif action == "2":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        network_addresses = input("Enter the Network addresses (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        ospf_area = input("Enter the OSPF area: ")
        
        routing_command += f"router ospf {router_ospf_process}\n"
        
        for network_address, wildcard_mask in zip(network_addresses, wildcard_masks):
            routing_command += f"network {network_address.strip()} {wildcard_mask.strip()} area {ospf_area}\n"
    
    elif action == "3":
        
        router_ospf_process = input("Enter the Router OSPF process number: ")
        ospf_area = input("Enter the OSPF area: ")
        router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        
        routing_command += f"router ospf {router_ospf_process}\n"
        routing_command += f"area {ospf_area} virtual-link {router_id}\n"
    
    elif action == "4":
        
        network_addresses = input("Enter the Network addresses (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        
        routing_command += "router eigrp 1\n"
        
        for network_address, wildcard_mask in zip(network_addresses, wildcard_masks):
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

def set_nat_pat(filtered_nr, password):
    
    print("********************\n")
    print("1 - Set NAT Static\n")
    print("2 - Set PAT 1 Public ip address\n")
    print("3 - Set PAT more than 1 Public ip address\n")
    print("4 - Set Out side\n")
    print("5 - Set In side\n")
    print("6 - Back\n")
    print("********************")
    action = input("Choose action : ")
    set_nat_pat_command = f"enable\n{password}\nconf t\n"
    
    if action == "1":
        
        private_ip_addresses = input("Enter the Private ip addresses (comma-separated): ").split(',')
        public_ip_addresses = input("Enter the Public ip addresses (comma-separated): ").split(',')
        
        for private_ip_addresses, public_ip_addresses in zip(private_ip_addresses, public_ip_addresses):
            set_nat_pat_command += f"ip nat inside source static {private_ip_addresses.strip()} {public_ip_addresses.strip()}\n"
    
    elif action == "2":
        
        ip_access_list_name = input("Enter the IP access list Standard name: ")
        network_addresses = input("Enter the Network addresses (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        interface = input("Enter the Out side interface (ex. f1/1): ")
        
        set_nat_pat_command += f"ip access-list standard {ip_access_list_name}\n"
        
        for network_address, wildcard_mask in zip(network_addresses, wildcard_masks):
            set_nat_pat_command += f"permit {network_address.strip()} {wildcard_mask.strip()}\n"
        
        set_nat_pat_command += f"ex\n"
        set_nat_pat_command += f"ip nat inside source list {ip_access_list_name} interface {interface} overload\n"
    
    elif action == "3":
        
        ip_access_list_name = input("Enter the IP access list Standard name: ")
        network_addresses = input("Enter the Network addresses (comma-separated): ").split(',')
        wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        ip_nat_pool_name = input("Enter the IP NAT pool name: ")
        public_ip_addresses_start = input("Enter the Public ip addresses (Start): ")
        public_ip_addresses_end = input("Enter the Public ip addresses (End): ")
        netmask_public_ip = input("Enter the Netmask Public ip addresses : ")
        
        set_nat_pat_command += f"ip access-list standard {ip_access_list_name}\n"
        
        for network_address, wildcard_mask in zip(network_addresses, wildcard_masks):
            set_nat_pat_command += f"permit {network_address.strip()} {wildcard_mask.strip()}\n"
        
        set_nat_pat_command += f"ex\n"
        set_nat_pat_command += f"ip nat pool {ip_nat_pool_name} {public_ip_addresses_start} {public_ip_addresses_end} netmask {netmask_public_ip}\n"
        set_nat_pat_command += f"ip nat inside source list {ip_access_list_name} pool {ip_nat_pool_name} overload\n"
    
    elif action == "4":
        interface = input("Enter the Out side interface (ex. f1/1): ")
        set_nat_pat_command += f"int {interface}\n"
        set_nat_pat_command += f"ip nat outside\n"
    
    elif action == "5":
        interface = input("Enter the In side interface (ex. f1/1): ")
        set_nat_pat_command += f"int {interface}\n"
        set_nat_pat_command += f"ip nat inside\n"
    
    elif action == "6":
        return
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def main():
    nr = InitNornir(config_file="config.yaml")
    
    filtered_nr = filter_group(nr)
    password = getpass("Enter Privileged Mode Password :")
    
    while True:
        print("********************\n")
        print("1 - Show Data\n")
        print("2 - Set VLAN\n")
        print("3 - Set Ether Channel\n")
        print("4 - Set Static  Routing\n")
        print("5 - Set Dynamic Routing\n")
        print("6 - Set NAT/PAT\n")
        print("7 - Exit\n")
        print("********************")        
        user_action = input("Choose action : ")
        
        if user_action == "1":
            show_data(filtered_nr, password)
        
        elif user_action == "2":
            set_vlan(filtered_nr, password)
        
        elif user_action == "3":
            set_ether_channel(filtered_nr, password)
        
        elif user_action == "4":
            set_static_routing(filtered_nr, password)
        
        elif user_action == "5":
            set_dynamic_routing(filtered_nr, password)
        
        elif user_action == "6":
            set_nat_pat(filtered_nr, password)
        
        elif user_action == "7":
            print("Exiting program...")
            break
        
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()