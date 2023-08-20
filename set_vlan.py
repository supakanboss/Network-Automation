from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_vlan_and_interface(filtered_nr):
    
    set_vlan_command = "enable\nconf t\n"
    
    vlan_num = input("Enter the VLAN Number: ")
    vlan_name = input("Enter the VLAN Name: ")
    interface = input("Enter the Interface (ex. f1/1-12): ")
        
    set_vlan_command += f"vlan {vlan_num}\n"
    set_vlan_command += f"name {vlan_name}\n"
    set_vlan_command += "ex\n"
    set_vlan_command += f"interface range {interface}\n"
    set_vlan_command += "switch mode access\n"
    set_vlan_command += f"switch access vlan {vlan_num}\n"
    
    result = filtered_nr.run(task=send_command, command=set_vlan_command)
    print_result(result) 
    filtered_nr.close_connections()

def set_trunk(filtered_nr):
    
    set_vlan_command = "enable\nconf t\n"

    vlan_num = input("Enter the VLAN Number: ")
    interface = input("Enter the Interface (ex. f1/1): ")
        
    set_vlan_command += f"interface {interface}\n"
    set_vlan_command += "switch mode trunk\n"
    set_vlan_command += f"switch trunk allowed vlan {vlan_num}\n"
    
    result = filtered_nr.run(task=send_command, command=set_vlan_command)
    print_result(result) 
    filtered_nr.close_connections()

def set_native_vlan(filtered_nr):
    
    set_vlan_command = "enable\nconf t\n"

    vlan_num = input("Enter the Native VLAN Number: ")
    interface = input("Enter the Trunk Interface (ex. f1/1): ")   
        
    set_vlan_command += f"interface {interface}\n"
    set_vlan_command += f"switch trunk native vlan {vlan_num}\n"
    
    result = filtered_nr.run(task=send_command, command=set_vlan_command)
    print_result(result) 
    filtered_nr.close_connections()

def set_ipv4_address_in_vlan(filtered_nr):
    
    set_vlan_command = "enable\nconf t\n"
    
    vlan_num = input("Enter the VLAN Number: ")
    network_address = input("Enter the IPv4 address: ")
    subnet = input("Enter the Subnet mask: ")
        
    set_vlan_command += f"interface vlan {vlan_num}\n"
    set_vlan_command += f"ip address {network_address} {subnet}\n"
    
    result = filtered_nr.run(task=send_command, command=set_vlan_command)
    print_result(result) 
    filtered_nr.close_connections()

def set_vlan(filtered_nr, group_name):
    
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Set VLAN")
    print("2 - Set Trunk")
    print("3 - Set Native VLAN")
    print("4 - Set IPv4 Address in VLAN")
    print("5 - Back\n")
    print("********************")
    action = input("Choose action: ")  
    
    if action == "1":
        set_vlan_and_interface(filtered_nr)
    
    elif action == "2":
        set_trunk(filtered_nr)
    
    elif action == "3":
        set_native_vlan(filtered_nr)
    
    elif action == "4":
        set_ipv4_address_in_vlan(filtered_nr)
    
    elif action == "5":
        return