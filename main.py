from nornir import InitNornir
from showdata import show_data
from backup_config import backup_config
from restore_config import restore_config
from automation_interface import automation_interface
from basic_interface import basic_interface
from connection_command import read_passwords_from_file, change_device_group

def main():
    
    global passwords

    nr = InitNornir(config_file="config.yaml")
    passwords = read_passwords_from_file('passwords.json')
    group_name, filtered_nr = change_device_group(nr, passwords)

    while True:
        print("******************** "+"---- \033[92mDevice Group : "+ group_name +"\033[0m -----\n")
        print("1 - Show Data")
        print("2 - Automation")
        print("3 - Basic Configuration")
        print("4 - Change Device Group")
        print("5 - Backup Config")
        print("6 - Restore Config")
        print("7 - Exit\n")
        print("********************")

        actions = {
            "1": lambda: show_data(filtered_nr, group_name),
            "2": lambda: automation_interface(filtered_nr, group_name),
            "3": lambda: basic_interface(filtered_nr, group_name),
            "4": lambda: change_device_group(nr, passwords),
            "5": lambda: backup_config(filtered_nr),
            "6": lambda: restore_config(filtered_nr),
            "7": lambda: exit("Exiting program...")
        }
        
        user_action = input("Choose action: ")

        if user_action in actions:
            actions[user_action]()
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    
    main()