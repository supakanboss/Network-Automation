from nornir import InitNornir
from showdata import show_data
from connection_command import check_device_status
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
        print("4 - Backup Config")
        print("5 - Restore Config")
        print("6 - Change Device Group")
        print("7 - Check Device Status")
        print("8 - Exit\n")
        print("********************")
        action = input("Choose action : ")

        if action == "1":
            show_data(filtered_nr, group_name)

        elif action == "2":
            automation_interface(filtered_nr, group_name)

        elif action == "3":
            basic_interface(filtered_nr, group_name)

        elif action == "4":
            backup_config(filtered_nr)

        elif action == "5":
            restore_config(filtered_nr)

        elif action == "6":
            group_name, filtered_nr = change_device_group(nr, passwords)

        elif action == "7":
            check_device_status(filtered_nr)

        elif action == "8":
            exit("Exiting program...")

        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
