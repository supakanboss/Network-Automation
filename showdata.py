from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def show_data_interface(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show interface"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_running_config(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show running-config"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_mac_address_table(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show mac address-table"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_vlan(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show vlan brief"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ip_interface(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ip interface brief"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ip_route(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ip route"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ospf_border_routers(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ospf border-routers"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ospf_neighbor(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ospf neighbor"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_eigrp_neighbor(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += f"show eigrp neighbor"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ipv6_interface(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ipv6 interface brief"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ipv6_route(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ipv6 route"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ipv6_ospf_neighbor(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ipv6 ospf neighbor"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_ip_nat_statistics(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show ip nat statistics"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_nat_translations(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show nat translations"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_access_list(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show access-list"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_interface_trunk(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show interface trunk"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_etherchannel_summary(filtered_nr):
    
    show_data_command = "enable\n"
    show_data_command += "show etherchannel summary"
    
    result = filtered_nr.run(task=send_command, command=show_data_command)
    print_result(result)
    filtered_nr.close_connections()

def show_data(filtered_nr, group_name):
    
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Show data interface")
    print("2 - Show running configuration")
    print("3 - Show Mac Address Table")
    print("4 - Show VLAN")
    print("5 - Show IP Interface")
    print("6 - Show IP Route")
    print("7 - Show IP OSPF Border routers")
    print("8 - Show IP OSPF Neighbor")
    print("9 - Show IP EIGRP Neighbors")
    print("10 - Show IPv6 Interface")
    print("11 - Show IPv6 Route")
    print("12 - Show IPv6 OSPF Neighbor")
    print("13 - Show IP NAT Statistics")
    print("14 - Show IP NAT Translations")
    print("15 - Show Access list")
    print("16 - Show Trunk Interface")
    print("17 - Show Ether Channel")
    print("18 - Back\n")
    print("********************")
    action = input("Choose action: ") 
    
    if action == "1":
        show_data_interface(filtered_nr)
        
    elif action == "2":
        show_running_config(filtered_nr)
        
    elif action == "3":
        show_mac_address_table(filtered_nr)
        
    elif action == "4":
        show_vlan(filtered_nr)
        
    elif action == "5":
        show_ip_interface(filtered_nr)
        
    elif action == "6":
        show_ip_route(filtered_nr)
        
    elif action == "7":
        show_ospf_border_routers(filtered_nr)
        
    elif action == "8":
        show_ospf_neighbor(filtered_nr)
        
    elif action == "9":
        show_eigrp_neighbor(filtered_nr)
        
    elif action == "10":
        show_ipv6_interface(filtered_nr)
        
    elif action == "11":
        show_ipv6_route(filtered_nr)
        
    elif action == "12":
        show_ipv6_ospf_neighbor(filtered_nr)
        
    elif action == "13":
        show_ip_nat_statistics(filtered_nr)
        
    elif action == "14":
        show_nat_translations(filtered_nr)
        
    elif action == "15":
        show_access_list(filtered_nr)
        
    elif action == "16":
        show_interface_trunk(filtered_nr)
    
    elif action == "17":
        show_etherchannel_summary(filtered_nr)
        
    elif action == "18":
        return
    
    else:
        print("Invalid selection. Please try again.")