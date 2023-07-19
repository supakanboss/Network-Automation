from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")

# Define the function to send Telnet commands using Netmiko
def send_telnet_command(task):
    show_interfaces_command = "show interfaces"  
    result_interfaces = task.run(task=netmiko_send_command, command_string=show_interfaces_command, use_timing=True)
    return {
        "interfaces": result_interfaces,
    }

# Get the group name from user input
group_name = input("Enter the device group name: ")

# Filter devices based on the provided group name
filtered_nr = nr.filter(F(groups__contains=group_name))

# Print the number of hosts after filtering
print(f"Number of hosts after filtering: {len(filtered_nr.inventory.hosts)}")

# Execute the task to send Telnet commands to the filtered devices
result = filtered_nr.run(task=send_telnet_command)

# Print the output
print_result(result)

# Close the connections
filtered_nr.close_connections()