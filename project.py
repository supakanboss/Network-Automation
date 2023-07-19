from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F
from getpass import getpass

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")

# Define the function to send commands using Netmiko
def send_command(task, command):
    result = task.run(task=netmiko_send_command, command_string=command, use_timing=True)
    return {
        "output": result,
    }

# Get the group name from user input
group_name = input("Enter the device group name: ")
# Filter devices based on the provided group name
filtered_nr = nr.filter(F(groups__contains=group_name))

# Print the number of hosts after filtering
print(f"Number of hosts after filtering: {len(filtered_nr.inventory.hosts)}")

# Ask user for action: show data or set routing
print("********************\n1 - Show Data\n2 - Set routing\n********************")
user_action = input("Choose action : ")
Password = getpass("Enter Privileged Mode Password :")

if user_action == "1":
    # Execute the task to send 'show interfaces' command to the filtered devices
    show_interfaces_command = f"enable\n{Password}\nshow int"
    result = filtered_nr.run(task=send_command, command=show_interfaces_command)

elif user_action == "2":
    
    # Ask user for routing protocol: OSPF or EIGRP
    print("********************\n1 - OSPF\n2 - EIGRP\n********************")
    routing_protocol = input("Choose routing protocol : ")
    
    # Ask user for multiple network addresses and wildcard masks
    network_addresses = input("Enter the network addresses (comma-separated): ").split(',')
    wildcard_masks = input("Enter the wildcard masks (comma-separated): ").split(',')

    routing_command = f"enable\n{Password}\nconf t\n"
    
    if routing_protocol == "1":
        # Ask user for OSPF area
        ospf_area = input("Enter the OSPF area : ")
        # Append OSPF command for each network
        routing_command += "router ospf 1\n"
        for network_address, wildcard_mask in zip(network_addresses, wildcard_masks):
            routing_command += f"network {network_address.strip()} {wildcard_mask.strip()} area {ospf_area}\n"
        
    elif routing_protocol == "2":
        # Append EIGRP command for each network
        routing_command += "router eigrp 1\n"
        for network_address, wildcard_mask in zip(network_addresses, wildcard_masks):
            routing_command += f"network {network_address.strip()} {wildcard_mask.strip()}\n"

    # Execute the task to send routing command to the filtered devices
    result = filtered_nr.run(task=send_command, command=routing_command)

# Print the output
print_result(result)
# Close the connections
filtered_nr.close_connections()
