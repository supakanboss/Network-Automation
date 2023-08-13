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

this script is a network automation tool. It uses Nornir, a Python framework, to manage and execute commands on network devices, and Netmiko for the actual communication with devices. The script allows users to interactively select a group of devices and execute various predefined tasks on those devices.

Initializes Nornir with a given config file.
Enters a loop allowing the user to specify a device group name and filters devices based on that name.
It checks the connectivity of devices in the group and moves on only if there are reachable devices.
Another loop presents a menu to the user with various network tasks like 'Show Data', 'Set IPv4 Address', 'Set VLAN', etc.
Depending on the user's choice, the respective function (which seems to be placeholders and might need further code) will be executed.
If the user selects to change the device group, it goes back to the group selection loop.
The program can be exited by selecting the 'Exit' option.