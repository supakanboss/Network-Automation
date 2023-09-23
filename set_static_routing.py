from showdata import show_ip_route
from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_static_routing(filtered_nr):
    
    network_address = input("Enter the Network address: ")
    subnet = input("Enter the Subnet mask: ")
    next_hop = input("Enter the Next hop: ")
    
    routing_command = "enable\nconf t\n"
    routing_command += f"ip route {network_address} {subnet} {next_hop}\n"
    
    result = filtered_nr.run(task=send_command, command=routing_command)
    print_result(result)
    filtered_nr.close_connections()
    show_ip_route(filtered_nr)