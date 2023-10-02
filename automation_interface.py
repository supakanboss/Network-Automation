from auto_generate_ip import auto_generate_ip
from auto_config_vlan import auto_config_vlan
from configure_svi_from_vlan import configure_svi_from_vlan
from showdata import show_ip_interface, show_vlan

def automation_interface(filtered_nr, group_name):
    print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
    print("1 - Auto Generate IP (Router)")
    print("2 - Auto Set VLAN")
    print("3 - Config SVI VLAN")
    print("4 - Show IP Interface")
    print("5 - Show VLAN")
    print("6 - Back\n")
    print("********************")
    
    action = input("Choose action: ") 
    
    if action == "1":
        auto_generate_ip(filtered_nr)
        
    elif action == "2":
        auto_config_vlan(filtered_nr)
        
    elif action == "3":
        configure_svi_from_vlan(filtered_nr)
        
    elif action == "4":
        show_ip_interface(filtered_nr)
        
    elif action == "5":
        show_vlan(filtered_nr)
        
    elif action == "6":
        return
    
    else:
        print("Invalid selection. Please try again.")