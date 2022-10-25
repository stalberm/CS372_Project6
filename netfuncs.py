import sys
import json
import re

def ipv4_to_value(ipv4_addr):
    """
    Convert a dots-and-numbers IP address to a single numeric value.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    ipv4_addr: "255.255.0.0"
    return:    0xffff0000 0b11111111111111110000000000000000 4294901760

    ipv4_addr: "1.2.3.4"
    return:    0x01020304 0b00000001000000100000001100000100 16909060
    """
    #Split on the dot
    ipv4_str = ipv4_addr.split(".")
    #Turn array of strings into list of ints
    ipv4_int = list(map(int, ipv4_str))
    #Go through the list and bit shift it by 8 times it's index from the right
    for i in list(range(0,len(ipv4_int))):
        #Index 0 is most significant, index at len-1 is least, that's why subtract i from max index
        #Index 0 = bit shift 3-0 * 8 = 24, index 3 = 3-3 * 8 = 0
        ipv4_int[i] = ipv4_int[i] << ((len(ipv4_int)-1-i)*8)

    #Bitwise OR all the values in the array
    value = ipv4_int[0]
    for i in list(range(1,len(ipv4_int))):
        value = value | ipv4_int[i]
    return value



def value_to_ipv4(addr):
    """
    Convert a single 32-bit numeric value to a dots-and-numbers IP
    address.

    Example:

    There is only one input value, but it is shown here in 3 bases.

    addr:   0xffff0000 0b11111111111111110000000000000000 4294901760
    return: "255.255.0.0"

    addr:   0x01020304 0b00000001000000100000001100000100 16909060
    return: "1.2.3.4"
    """
    #Bit shift the number by 8 * its index from the right (we know 3 is max index) and AND with max val
    ipv4 = []
    for i in range(3,-1,-1):
        ipv4.append(addr >> (i*8) & 255)
    #Turn the list of ints to list of strings and join them with dots between them
    ipv4 = list(map(str, ipv4))
    ipv4 = ".".join(ipv4)
    return ipv4

def get_subnet_mask_value(slash):
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number. The input can contain an IP address optionally,
    but that part should be discarded.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111111111110000000000000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """

    #Split whats passed in on the slash and grab the value to the right of the slash
    network = slash.split('/')
    network = int(network[1])
    #Host bits are 32 minus the network bits
    host = 32-network
    #Thinking in binary, get a string of n 1s where n = network
    mask = (2**network)-1
    #Add host number of 0s by shifting it over host times
    return mask << host

def ips_same_subnet(ip1, ip2, slash):
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notataion, return true if the two IP addresses are on the same
    subnet.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """

    subnet_mask = get_subnet_mask_value(slash)

    ipv4_1 = ipv4_to_value(ip1)
    ipv4_2 = ipv4_to_value(ip2)
    
    #And the ip value and subnet mask value to get the network
    val1 = ipv4_1 & subnet_mask
    val2 = ipv4_2 & subnet_mask
    return (val1 == val2)

def get_network(ip_value, netmask):
    """
    Return the network portion of an address value.

    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300
    """

    network = ip_value & netmask
    return network

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """


    for key, value in routers.items():
        #key is the ip, and value['netmask'] is it's corresponding slash value
        if ips_same_subnet(key,ip,value['netmask']):
            return key

    return None


# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!

# def my_tests():
#     print("-------------------------------------")
#     print("This is the result of my custom tests")
#     print("-------------------------------------")
    
#     routers = {
#         "1.2.3.1": {
#             "netmask": "/24"
#         },
#         "1.2.4.1": {
#             "netmask": "/24"
#         }
#     }
#     ip = "1.2.5.6"
#     print(find_router_for_ip(routers, ip))


## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = find_router_for_ip(routers, ip)
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
