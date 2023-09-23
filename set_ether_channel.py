from showdata import show_etherchannel_summary
from connection_command import send_command
from nornir_utils.plugins.functions import print_result

def set_ether_channel(filtered_nr):
    
    interface = input("Enter the Interface (e.g., f1/1-12): ")
    channel_group_number = input("Enter the Channel group number: ")
    vlan_number = input("Enter the VLAN Number: ")
    
    set_ether_channel_command = "enable\nconf t\n"
    
    set_ether_channel_command += f"interface range {interface}\n"
    set_ether_channel_command += f"channel-group {channel_group_number} mode active\n"
    set_ether_channel_command += "ex\n"
    set_ether_channel_command += f"interface port-channle {channel_group_number}\n"
    set_ether_channel_command += "switch mode trunk\n"
    set_ether_channel_command += f"switch trunk allowed vlan {vlan_number}\n"
    
    result = filtered_nr.run(task=send_command, command=set_ether_channel_command)
    print_result(result)
    filtered_nr.close_connections()
    show_etherchannel_summary(filtered_nr)