from getpass import getpass
from connection_command import test_connection, ConnectHandler

def backup_config(filtered_nr):
    
    print("Starting config backup...")
    command = "show running-config"

    for host in filtered_nr.inventory.hosts.values():
        netmiko_params = host.get_connection_parameters("netmiko")
        netmiko_params = netmiko_params.dict()  

        netmiko_params.pop("extras", None)  
        netmiko_params["host"] = netmiko_params.pop("hostname", None)  
        netmiko_params.pop("platform", None)  
        netmiko_params["device_type"] = host.platform

        host_ip = host.hostname

        if not test_connection(host_ip):
            print("\033[91m" + f"Cannot connect to device {host} , skipping...\n" + "\033[0m")
            continue

        enable_password = getpass(f"Enter enable password for \033[33m{host}\033[0m: ")
        netmiko_params["secret"] = enable_password

        file_name = input(f"Enter the filename to save the backup for \033[33m{host}\033[0m (without extension): ")

        try:
            with ConnectHandler(**netmiko_params) as conn:
                conn.enable()  
                output = conn.send_command(command)
                with open(f"backup/{file_name}-{host}.conf", "w") as file:
                    file.write(output)
                    print(f"\033[92mConfig for {host} saved to {file_name}.conf!\033[0m")
        except Exception as e:
            print(f"\033[91mAn error occurred while backing up {host}: {e}\033[0m")

    print("\033[92mConfig backup complete.\033[0m")