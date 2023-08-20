from nornir import InitNornir
from showdata import show_data
from auto_generate_ip import auto_generate_ip
from set_ipv4 import set_ipv4
from auto_config_vlan import auto_config_vlan
from set_vlan import set_vlan
from set_ether_channel import set_ether_channel
from set_static_routing import set_static_routing
from set_dynamic_routing import set_dynamic_routing
from set_dhcp import set_dhcp
from set_nat_pat import set_nat_pat
from set_ipv6 import ipv6
from backup_config import backup_config
from restore_config import restore_config
from connection_command import read_passwords_from_file, change_device_group

def main():
    
    global passwords

    nr = InitNornir(config_file="config.yaml")
    passwords = read_passwords_from_file('passwords.json')
    group_name, filtered_nr = change_device_group(nr, passwords)

    while True:
        print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
        print("1 - Show Data")
        print("2 - Auto Set IPv4 Address")
        print("3 - Set IPv4 Address")
        print("4 - Auto Set VLAN")
        print("5 - Set VLAN")
        print("6 - Set Ether Channel")
        print("7 - Set Static  Routing")
        print("8 - Set Dynamic Routing")
        print("9 - Set DHCP")
        print("10 - Set NAT/PAT")
        print("11 - IPv6")
        print("12 - Change Device Group")
        print("13 - Backup Config")
        print("14 - Restore Config")
        print("15 - Exit\n")
        print("********************")

        actions = {
            "1": lambda: show_data(filtered_nr, group_name),
            "2": lambda: auto_generate_ip(filtered_nr),
            "3": lambda: set_ipv4(filtered_nr),
            "4": lambda: auto_config_vlan(filtered_nr),
            "5": lambda: set_vlan(filtered_nr, group_name),
            "6": lambda: set_ether_channel(filtered_nr),  
            "7": lambda: set_static_routing(filtered_nr),  
            "8": lambda: set_dynamic_routing(filtered_nr, group_name),
            "9": lambda: set_dhcp(filtered_nr, group_name),
            "10": lambda: set_nat_pat(filtered_nr, group_name),
            "11": lambda: ipv6(filtered_nr, group_name),
            "12": lambda: change_device_group(nr, passwords),
            "13": lambda: backup_config(filtered_nr),
            "14": lambda: restore_config(filtered_nr),
            "15": lambda: exit("Exiting program...")
        }
        
        user_action = input("Choose action: ")

        if user_action in actions:
            actions[user_action]()
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    
    main()