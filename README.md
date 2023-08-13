# Network-Automation

Installation Guide

To set up the necessary environment for your Python script, you'll need to install the following libraries:

## 1. Nornir
[Nornir](https://nornir.tech/) is a Python framework that helps with automating networks.

```bash
pip install nornir
```

## 2. Netmiko
[Netmiko](https://github.com/ktbyers/netmiko) is a library to simplify the process of connecting to devices using SSH.

```bash
pip install netmiko
```

## 3. Nornir Utils
[Nornir Utils](https://github.com/nornir-automation/nornir_utils) provides utility plugins for Nornir.

```bash
pip install nornir_utils
```

After installing the above libraries, your script ready to run!

this script is a network automation tool. It uses Nornir, a Python framework, to manage and execute commands on network devices, and Netmiko for the actual communication with devices. The script allows users to interactively select a group of devices and execute various tasks on those devices.

Initialization:
    > Initializes Nornir with the given configuration file.
    > Reads device passwords from a JSON file.

Device Group Selection:
    > In a loop, prompts the user to specify a device group name.
    > Filters and checks connectivity for devices in that group.
    > Proceeds only if there are reachable devices in the selected group.

Task Menu:
    > Presents a menu of network tasks (e.g., 'Show Data', 'Set IPv4 Address').
    > Executes the respective function based on the user's choice.
    > Offers an option to switch device groups, which returns to the device group selection loop.
    > Allows for program exit.