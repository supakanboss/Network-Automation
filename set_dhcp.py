from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_dhcp_pool(filtered_nr):
    
    dhcp_command = "enable\nconf t\n"
    
    dhcp_pool_name = input("Enter the DHCP Pool Name: ")
    network_address = input("Enter the Network Address: ")
    subnet = input("Enter the Subnet mask: ")
        
    dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
    dhcp_command += f"network {network_address} {subnet}\n"
    
    result = filtered_nr.run(task=send_command, command=dhcp_command)
    print_result(result)
    filtered_nr.close_connections()

def set_excluded_ip_address(filtered_nr):
    
    dhcp_command = "enable\nconf t\n"
    
    network_address = input("Enter the Network Address (comma-separated): ").split(',')
        
    for network_address in zip(network_address):
        dhcp_command += f"ip dhcp excluded-address {network_address.strip()}\n"
    
    result = filtered_nr.run(task=send_command, command=dhcp_command)
    print_result(result)
    filtered_nr.close_connections()

def optional_default_router(filtered_nr):
    
    dhcp_command = "enable\nconf t\n"
    
    dhcp_pool_name = input("Enter the DHCP Pool Name: ")
    default_router_ip_address = input("Enter the Default Gateway IP Address: ")
    
    dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
    dhcp_command += f"default-router {default_router_ip_address}\n"
    
    result = filtered_nr.run(task=send_command, command=dhcp_command)
    print_result(result)
    filtered_nr.close_connections()

def optional_dns_server(filtered_nr):
    
    dhcp_command = "enable\nconf t\n"
    
    dhcp_pool_name = input("Enter the DHCP Pool Name: ")
    dns_server_ip_address = input("Enter the DNS Server IP Address: ")
        
    dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
    dhcp_command += f"dns-server {dns_server_ip_address}\n"
    
    result = filtered_nr.run(task=send_command, command=dhcp_command)
    print_result(result)
    filtered_nr.close_connections()

def optional_lease(filtered_nr):
    
    dhcp_command = "enable\nconf t\n"
    
    dhcp_pool_name = input("Enter the DHCP Pool Name: ")
    lease_duration_minutes = input("Enter the Lease Duration Minutes: ")
        
    dhcp_command += f"ip dhcp pool {dhcp_pool_name}\n"
    dhcp_command += f"lease {lease_duration_minutes}\n"
    
    result = filtered_nr.run(task=send_command, command=dhcp_command)
    print_result(result)
    filtered_nr.close_connections()

def set_dhcp(filtered_nr, group_name):

    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Set DHCP Pool")
    print("2 - Set Excluded IP Address")
    print("3 - Optional Default Router")
    print("4 - Optional DNS Server")
    print("5 - Optional Set the lease duration for clients in minutes")
    print("6 - Back\n")
    print("********************")
    action = input("Choose action : ")
    
    if action == "1":
        set_dhcp_pool(filtered_nr)
    
    elif action == "2":
        set_excluded_ip_address(filtered_nr)
    
    if action == "3":
        optional_default_router(filtered_nr)
    
    if action == "4":
        optional_dns_server(filtered_nr)
    
    if action == "5":
        optional_lease(filtered_nr)
    
    if action == "6":
        return
    
    else:
        print("Invalid selection. Please try again.")