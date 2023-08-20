from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_router_id(filtered_nr):
    
    routing_command = "enable\nconf t\n"
    
    router_ospf_process = input("Enter the Router OSPF process number: ")
    router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
    
    routing_command += f"router ospf {router_ospf_process}\n"
    routing_command += f"router-id {router_id}\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_ospf(filtered_nr):
    
    routing_command = "enable\nconf t\n"
    
    router_ospf_process = input("Enter the Router OSPF process number: ")
    network_address = input("Enter the Network address (comma-separated): ").split(',')
    wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
    ospf_area = input("Enter the OSPF area: ")
        
    routing_command += f"router ospf {router_ospf_process}\n"
        
    for network_address, wildcard_mask in zip(network_address, wildcard_masks):
        routing_command += f"network {network_address.strip()} {wildcard_mask.strip()} area {ospf_area}\n"
    
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_virtual_link(filtered_nr):
    
    routing_command = "enable\nconf t\n"
    
    router_ospf_process = input("Enter the Router OSPF process number: ")
    ospf_area = input("Enter the OSPF area: ")
    router_id = input("Enter the Router ID (ex. 1.1.1.1): ")
        
    routing_command += f"router ospf {router_ospf_process}\n"
    routing_command += f"area {ospf_area} virtual-link {router_id}\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_eigrp(filtered_nr):
    
    routing_command = "enable\nconf t\n"
    
    router_eigrp_process = input("Enter the Router EIGRP process number: ")
    network_address = input("Enter the Network address (comma-separated): ").split(',')
    wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
        
    routing_command += f"router eigrp {router_eigrp_process}\n"
        
    for network_address, wildcard_mask in zip(network_address, wildcard_masks):
        routing_command += f"network {network_address.strip()} {wildcard_mask.strip()}\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_redistribute(filtered_nr):
    
    routing_command = "enable\nconf t\n"
    
    router_ospf_process = input("Enter the Router OSPF process number: ")
    router_eigrp_process = input("Enter the Router EIGRP process number: ")
        
    routing_command += f"router ospf {router_ospf_process}\n"
    routing_command += f"redistribute eigrp {router_eigrp_process} subnets\n"
    routing_command += f"router eigrp {router_eigrp_process}\n"
    routing_command += f"redistribute ospf {router_eigrp_process} metric 1000 10 255 1 1500\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def clear_ospf_process(filtered_nr):
    
    routing_command = "enable\nconf t\n"
    
    routing_command += "do clear ip ospf process\n"
    routing_command += "yes\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()

def set_dynamic_routing(filtered_nr, group_name):
    
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Set Router ID")
    print("2 - Set OSPF")
    print("3 - Set Virtual Link")
    print("4 - Set EIGRP")
    print("5 - Set Redistribute")
    print("6 - Clear OSPF process")
    print("7 - Back\n")
    print("********************")
    action = input("Choose action : ")
    
    if action == "1":
        set_router_id(filtered_nr)
    
    elif action == "2":
        set_ospf(filtered_nr)
    
    elif action == "3":
        set_virtual_link(filtered_nr)
    
    elif action == "4":
        set_eigrp(filtered_nr)
    
    elif action == "5":
        set_redistribute(filtered_nr)
    
    elif action == "6":
        clear_ospf_process(filtered_nr)
    
    elif action == "7":
        return