from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_ipv6_address_in_interface(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    interface = input("Enter the Interface (ex. f1/1): ")
    address = input("Enter the IPv6 address: ")
    prefix_lengths = input("Enter the Prefix Lengths: ")
    
    ipv6_command += "ipv6 unicast-routing\n"
    ipv6_command += f"interface {interface}\n"
    ipv6_command += "no shutdown\n"
    ipv6_command += "no switchport\n"
    ipv6_command += f"ipv6 address {address}/{prefix_lengths}\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ipv6_address_in_vlan(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    vlan_number = input("Enter the VLAN Nmuber: ")
    address = input("Enter the IPv6 address: ")
    prefix_lengths = input("Enter the Prefix Lengths: ")
    
    ipv6_command += "ipv6 unicast-routing\n"
    ipv6_command += f"interface vlan {vlan_number}\n"
    ipv6_command += f"ipv6 address {address}/{prefix_lengths}\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ipv6_eui64(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    interface = input("Enter the Interface (ex. f1/1 or vlan 10): ")
    address = input("Enter the IPv6 address: ")
    prefix_lengths = input("Enter the Prefix Lengths: ")
    
    ipv6_command += "ipv6 unicast-routing\n"
    ipv6_command += f"interface {interface}\n"
    ipv6_command += f"ipv6 address {address}/{prefix_lengths} eui-64\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ipv6_tunnel(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    tunnel_number = input("Enter the Interface Tunnel Number: ")
    address = input("Enter the IPv6 address: ")
    prefix_lengths = input("Enter the Prefix Lengths: ")
    tunnel_source = input("Enter the Tunnel Source (ex. g0/0/0): ")
    tunnel_destination = input("Enter the Tunnel Destination (IPv4 Address): ")
        
    ipv6_command += f"interface tunnel {tunnel_number}\n"
    ipv6_command += f"ipv6 address {address}/{prefix_lengths}\n"
    ipv6_command += f"tunnel source {tunnel_source}\n"
    ipv6_command += f"tunnel destination {tunnel_destination}\n"
    ipv6_command += "tunnel tunnel mode ipv6ip\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ipv6_router_id(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    ospfv3_process_number = input("Enter the Router OSPFv3 process number: ")
    router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        
    ipv6_command += f"ipv6 router ospf {ospfv3_process_number}\n"
    ipv6_command += f"router-id {router_id}\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ipv6_ospf3(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    ospfv3_process_number = input("Enter the Router OSPFv3 process number: ")
    interface = input("Enter the Interface (ex. f1/1-10,f1/14): ")
    ospfv3_area = input("Enter the OSPFv3 area: ")
        
    ipv6_command += f"interface {interface}\n"
    ipv6_command += f"ipv6 ospf {ospfv3_process_number} area {ospfv3_area}\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def clear_ipv6_ospf_process(filtered_nr):
    
    ipv6_command = "enable\nconf t\n"
    
    ipv6_command += "do clear ipv6 ospf process\n"
    ipv6_command += "yes\n"
    
    result = filtered_nr.run(task=send_command, command=ipv6_command)
    print_result(result)
    filtered_nr.close_connections()

def ipv6(filtered_nr, group_name):
    
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
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
    
    if action == "1":
        set_ipv6_address_in_interface(filtered_nr)

    elif action == "2":
        set_ipv6_address_in_vlan(filtered_nr)
    
    elif action == "3":
        set_ipv6_eui64(filtered_nr)

    elif action == "4":
        set_ipv6_tunnel(filtered_nr)
    
    elif action == "5":
        set_ipv6_router_id(filtered_nr)
    
    elif action == "6":
        set_ipv6_ospf3(filtered_nr)
    
    elif action == "7":
        clear_ipv6_ospf_process(filtered_nr)
    
    elif action == "8":
        return