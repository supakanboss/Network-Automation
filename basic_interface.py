from set_ipv6 import ipv6
from set_ipv4 import set_ipv4
from set_vlan import set_vlan
from set_dhcp import set_dhcp
from set_nat_pat import set_nat_pat
from set_ether_channel import set_ether_channel
from set_static_routing import set_static_routing
from set_dynamic_routing import set_dynamic_routing

def basic_interface(filtered_nr, group_name):
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Set IPv4")
    print("2 - Set VLAN")
    print("3 - Set Ether Channel")
    print("4 - Set Static Routing")
    print("5 - Set Dynamic Routing")
    print("6 - Set DHCP")
    print("7 - Set NAT/PAT")
    print("8 - Set IPv6")
    print("9 - Back\n")
    print("********************")
    
    action = input("Choose action: ") 
    
    if action == "1":
        set_ipv4(filtered_nr)
        
    elif action == "2":
        set_vlan(filtered_nr, group_name)
        
    elif action == "3":
        set_ether_channel(filtered_nr)
        
    elif action == "4":
        set_static_routing(filtered_nr)
        
    elif action == "5":
        set_dynamic_routing(filtered_nr, group_name)
        
    elif action == "6":
        set_dhcp(filtered_nr, group_name)
        
    elif action == "7":
        set_nat_pat(filtered_nr, group_name)
        
    elif action == "8":
        ipv6(filtered_nr, group_name)
                
    elif action == "9":
        return