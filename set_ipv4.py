from connection_command import send_command
from nornir_utils.plugins.functions import print_result

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