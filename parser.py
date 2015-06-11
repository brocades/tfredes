from common.addr_class import AddrClass

from enum import Enum
from classes import *

import sys

class ParserState(Enum):
    NETWORK = 1
    ROUTER = 2


filename = sys.argv[2]
first_address_type = sys.argv[3]
topologia = open(filename, 'r')
g_networks = []
g_routers = []
parseState = None

"""
#networks_bits = []
#is_reading_networks = True
#default_mask_number = "255"

# Parse first address and IP class
address_aux = first_address_type.strip().split('/')
first_address = address_aux[0]
address_class = address_aux[1]


# Returns the number of bits needed the represent the amount of hosts the network needs
def number_of_bits(integer):
    a = int(integer)
    bits_length = a.bit_length()
    pow_of_two = pow(2, bits_length)
    if pow_of_two - 2 < int(integer):
        return bits_length + 1
    return bits_length


# Returns a list with the number of bits needed to represent the amount of hosts the network needs
# for each network
def list_number_of_bits(networks):
    for net in networks:
        min_number_of_hosts = pow(2, number_of_bits(net[1]))
        networks_bits.append(tuple([net[0], min_number_of_hosts]))


# Tells how many bits are necessary for subnet
def bits_for_subnetwork(integer):
    a = int(integer)
    return a.bit_length()


def define_subnetmask(address_class, routers):
    subnetmask_net = []
    first_router = routers[0]
    # for net in networks_bits:
    addr_class = int(address_class) + bits_for_subnetwork(first_router[1])
    number_of_defaults = addr_class // 8
    addr_remainder = addr_class % 8
    subnetmask = (default_mask_number + ".") * number_of_defaults
    return subnetmask

#topologia.close()
#list_number_of_bits(networks)
#print(define_subnetmask(address_class, routers))
#print(networks_bits)
#print(networks)
#print(routers)
#print(first_address)
#print(address_class)
#print(AddrClass.which_class(address_class))
"""

# Removes white spaces and line endings
def clean_line(line):
    return line.strip().replace(" ", "")

firstAddress = first_address_type.split("/")

networkIndex = 0

# Parses networks and routers
for line in topologia.readlines():

    if line.strip() == "#NETWORK":
        parseState = ParserState.NETWORK
    elif line.strip() == "#ROUTER":
        parseState = ParserState.ROUTER

    if line.strip()[0:1] != "#":

        if parseState == ParserState.NETWORK:
            networkLines = clean_line(line).split(',')
            g_networks.append(Network(networkLines[0], int(networkLines[1]), networkIndex))
            networkIndex += 1

        elif parseState == ParserState.ROUTER:
            configLines = clean_line(line).split(',')
            newRouter = Router(configLines[0], int(configLines[1]))

            numberOfNetworks = int(configLines[1])
            networks = []
            for x in range(0, numberOfNetworks):
                networks.append(configLines[2+x])

            newRouter.m_networkNames = networks

            g_routers.append(newRouter)


addressBase = IPAddress(firstAddress[0], int(firstAddress[1]))

alloc = NetworkAlloc()

g_networks = alloc.getNetworksIPs(g_networks, addressBase)

g_networks = sorted(g_networks, key=lambda x: x.m_index, reverse=False)

#print(addressBase.m_address)
#print(addressBase.m_address.getOffsetAddress(1024))
#print(addressBase.m_address.getOffsetAddress(2048))
#print(addressBase.m_address.getOffsetAddress(25))
#print(addressBase.m_address.getOffsetAddress(10025))

#addressBase.getNetworksIPs(g_networks)

print("\n" + "--- RESULT ---" + "\n")

print("#NETWORK")
for network in g_networks:
    print(network.getResultStr())
print("#ROUTER")
for router in g_routers:
    router.getNetworks(g_networks)
    print(router.getResultStr())
print("#ROUTERTABLE")
for router in g_routers:
    router.getRemainingNetworks(g_networks)
    print(router.getRouterTableResultStr())