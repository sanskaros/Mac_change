#!/bin/usr/env python
import subprocess
import optparse
import re
#all the fuctionality is encapsulated in the tow function code is much cleaner.
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="specify the Interface for changing it's Mac")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter the new Mac Address")
    (options, arguments)= parser.parse_args()
    if not options.interface:
        parser.error("please specify an interface or use --help for more information")
    elif not options.new_mac:
        parser.error("please specify a new mac address or use --help for more information")
    return options
def change_mac(interface,new_mac):
    print("[+] changing mac address of the interface " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "down"])
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w ", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] we could not change mac address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[+] Current MAC is " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Current MAC successfully changed to " + current_mac)
else:
    print("[-] Mac address is unchanged .")
