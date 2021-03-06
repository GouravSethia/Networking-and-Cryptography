#! usr/bin/env python3
import subprocess                       # To execute terminal commands
import optparse                         # To parse ouput of ifcongif
import re                               # To read ether value from output of ifconfig

def get_arguments():
    parser = optparse.OptionParser()
    # To let user specify inetrface and new MAC address:
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    # To check all values are entered correctly:
    if not options.interface:
        parser.error("[-] Please enter the interface!, use --help for more info")
    if not options.new_mac:
        parser.error("[-] Please enter a new MAC address!, use --help for more info")
    return options
# Main code to change MAC address:
def change_mac(interface,new_mac):
    print("[+] Changing MAC for " + interface)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

# Parsing output of ifconfig to get ether value (the MAC address)    
def get_current_mac(interface):
    ifconfig_result=subprocess.check_output(["ifconfig", interface])
    mac_address_search_result= re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not find MAC address!")

options = get_arguments()
current_mac= get_current_mac(options.interface)
print("Current MAC address: " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac= get_current_mac(options.interface)
if current_mac==options.new_mac:
    print("[+] MAC address was successfully changed to "+current_mac)
else:
    print("[-] MAC address did not get changed!")
