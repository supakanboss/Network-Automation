from showdata import show_ip_nat_statistics, show_nat_translations, show_access_list
from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_nat_static(filtered_nr):
    
    set_nat_pat_command = "enable\nconf t\n"
    
    private_ip_address = input("Enter the Private ip address (comma-separated): ").split(',')
    public_ip_address = input("Enter the Public ip address (comma-separated): ").split(',')
        
    for private_ip_address, public_ip_address in zip(private_ip_address, public_ip_address):
        set_nat_pat_command += f"ip nat inside source static {private_ip_address.strip()} {public_ip_address.strip()}\n"
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def set_pat_one_public_ip_address(filtered_nr):
    
    set_nat_pat_command = "enable\nconf t\n"
    
    ip_access_list_name = input("Enter the IP access list Standard name: ")
    network_address = input("Enter the Network address (comma-separated): ").split(',')
    wildcard_masks = input("Enter the Wildcard masks (comma-separated): ").split(',')
    interface = input("Enter the Out side interface (e.g., f1/1): ")
        
    set_nat_pat_command += f"ip access-list standard {ip_access_list_name}\n"
        
    for network_address, wildcard_mask in zip(network_address, wildcard_masks):
        set_nat_pat_command += f"permit {network_address.strip()} {wildcard_mask.strip()}\n"
        
    set_nat_pat_command += f"ex\n"
    set_nat_pat_command += f"ip nat inside source list {ip_access_list_name} interface {interface} overload\n"
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def set_patmore_than_one_public_ip_address(filtered_nr):
    
    set_nat_pat_command = "enable\nconf t\n"
    
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
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def set_out_side(filtered_nr):
    
    set_nat_pat_command = "enable\nconf t\n"
    
    interface = input("Enter the NAT Out-side Interface (e.g., f1/1): ")
    set_nat_pat_command += f"interface {interface}\n"
    set_nat_pat_command += "ip nat outside\n"
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def set_in_side(filtered_nr):
    
    set_nat_pat_command = "enable\nconf t\n"
    
    interface = input("Enter the NAT In-side Interface (e.g., f1/1): ")
    set_nat_pat_command += f"interface {interface}\n"
    set_nat_pat_command += "ip nat inside\n"
    
    result = filtered_nr.run(task=send_command, command=set_nat_pat_command)
    print_result(result)
    filtered_nr.close_connections()

def set_nat_pat(filtered_nr, group_name):
    
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Set NAT Static")
    print("2 - Set PAT 1 Public ip address")
    print("3 - Set PAT more than 1 Public ip address")
    print("4 - Set Out side")
    print("5 - Set In side\n")
    print("6 - Show IP NAT Statistics")
    print("7 - Show IP NAT Translations")
    print("8 - Show Access list")
    print("9 - Back\n")
    print("********************")
    action = input("Choose action : ")
    
    if action == "1":
        set_nat_static(filtered_nr)
    
    elif action == "2":
        set_pat_one_public_ip_address(filtered_nr)
    
    elif action == "3":
        set_patmore_than_one_public_ip_address(filtered_nr)
    
    elif action == "4":
        set_out_side(filtered_nr)
    
    elif action == "5":
        set_in_side(filtered_nr)
    
    elif action == "6":
        show_ip_nat_statistics(filtered_nr)
        
    elif action == "7":
        show_nat_translations(filtered_nr)
        
    elif action == "8":
        show_access_list(filtered_nr)
    
    elif action == "9":
        return