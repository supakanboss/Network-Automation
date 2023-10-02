import json
import logging
import traceback
from nornir.core.filter import F
from netmiko import ConnectHandler

def test_connection(host):
    
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, 23))  
        s.close()
        print(f"\033[92mSuccessfully connected to device {host} \033[0m")
        return True
    except Exception as e:
        print(f"\033[91mCannot connect to device {host} : {e} \033[0m")
        return False

def read_passwords_from_file(filename):
    
    with open(filename, 'r') as file:
        data = json.load(file)
        return data

def custom_exception_handler(e, device_name):
    
    frames = traceback.extract_tb(e.__traceback__)
    frame = frames[-1]  
    filename = frame.filename.split("\\")[-1]  
    lineno = frame.lineno
    line = frame.line.strip()
    message = f"ERROR on device '{device_name}': {filename}:{lineno} - {line} => {e}"
    logging.error(f"\033[91m {message} \033[0m")
    return message

def send_command(task, command):
    
    device_name = task.host.name

    passwords = read_passwords_from_file("passwords.json")
    password = passwords.get(device_name)

    net_connect = None

    if password is None:
        logging.error(f"\033[91m Password not found for {device_name} \033[0m")
        return "Password not found for device"
    
    if not test_connection(task.host.hostname):
        logging.error(f"\033[91m Cannot connect to {device_name} \033[0m")  
        return "Cannot connect to device"

    device_type = task.host.get('device_type', 'cisco_ios_telnet')
    
    try:
        net_connect = ConnectHandler(device_type=device_type, ip=task.host.hostname, username=task.host.username, password=password)
        result = net_connect.send_command_timing("enable")
        if "Password:" in result:  
            result += net_connect.send_command_timing(password)
        result += net_connect.send_command_timing(command)
        print(f"\033[92mConnected to device {device_name}\033[0m")
    except Exception as e:
        result = custom_exception_handler(e, device_name)
    finally:
        if net_connect:
            net_connect.disconnect()

    return result

def send_command_host(host, command):
    
    device_name = host.name

    passwords = read_passwords_from_file("passwords.json")
    password = passwords.get(device_name)

    net_connect = None

    if password is None:
        logging.error(f"\033[91m Password not found for {device_name} \033[0m")
        return "Password not found for device"
    
    if not test_connection(host.hostname):
        logging.error(f"\033[91m Cannot connect to {device_name} \033[0m")  
        return "Cannot connect to device"

    device_type = host.get('device_type', 'cisco_ios_telnet')
    
    try:
        net_connect = ConnectHandler(device_type=device_type, ip=host.hostname, username=host.username, password=password)
        result = net_connect.send_command_timing("enable")
        if "Password:" in result:  
            result += net_connect.send_command_timing(password)
        result += net_connect.send_command_timing(command)
        print(f"\033[92mConnected to device {device_name}\033[0m")
    except Exception as e:
        result = custom_exception_handler(e, device_name)
    finally:
        if net_connect:
            net_connect.disconnect()

    return result

def filter_group(nr, group_name):    
    
    filtered_nr = nr.filter(F(groups__contains=group_name))
    hosts = filtered_nr.inventory.hosts
    num_hosts = len(hosts)
    
    if num_hosts > 0:
        print(f"Number of hosts after filtering: {num_hosts}")
        print("Devices in group \033[33m{}\033[0m:".format(group_name))
        return filtered_nr, hosts
    else:
        print("No devices found in group \033[33m{}\033[0m.".format(group_name))
        return None, None

def check_device_status(nr):
    print(f"Checking status of devices in the group:")
    
    filtered_nr = nr.filter(F(groups__contains="all"))
    active_devices = []
    inactive_devices = []
    
    for host in filtered_nr.inventory.hosts.values():
        host_ip = host.hostname
        if test_connection(host_ip):
            active_devices.append(host.name)
        else:
            inactive_devices.append(host.name)
    
    print("\nActive devices:")
    for device in active_devices:
        print(f"\033[92m{device}\033[0m is active")
    
    print("\nInactive devices:")
    for device in inactive_devices:
        print(f"\033[91m{device}\033[0m is inactive")


def change_device_group(nr, passwords):
    
    while True:
        group_name = input("Enter the device group name: ")
        filtered_nr, hosts = filter_group(nr, group_name)

        if filtered_nr is not None:
            connected_devices = []
            for host in hosts:
                host_ip = nr.inventory.hosts[host].hostname
                if test_connection(host_ip):
                    if host not in passwords:
                        print(f"\033[91mPassword for device {host} not found in file, skipping...\033[0m\n")
                        continue
                    connected_devices.append(host)
                    print(f"\033[92mConnected to device {host} successfully!\033[0m\n")
                else:
                    print(f"\033[91mCannot connect to device {host}, skipping...\033[0m\n")

            if connected_devices:
                return group_name, filtered_nr
            else:
                print("No devices in this group could be connected to. Please choose another group.\n")
        else:
            print("Invalid device group. Please enter a valid group name.")