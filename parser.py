from common.addr_class import AddrClass
import sys

filename = sys.argv[1]
first_address_type = sys.argv[2]
topologia = open(filename, 'r')
networks = []
routers = []
networks_bits = []
is_reading_networks = True

# Parse first address and IP class
address_aux = first_address_type.strip().split('/')
first_address = address_aux[0]
address_class = address_aux[1]

# Removes white spaces and line endings
def clean_line(line):
	return line.strip().replace(" ","")

# Returns the number of bits needed the represent the amount of hosts the network needs
def number_of_bits(integer):
	a = int(integer)
	bits_length = a.bit_length()
	pow_of_two = pow(2,bits_length)
	if pow_of_two-2 < int(integer):
		return bits_length + 1
	return bits_length

# Returns a list with the number of bits needed to represent the amount of hosts the network needs
# for each network
def list_number_of_bits(networks):
	for net in networks:
		min_number_of_hosts = pow(2,number_of_bits(net[1]))
		networks_bits.append(tuple([net[0],min_number_of_hosts]))

# Parses networks and routers
for line in topologia.readlines():
	if line.strip() == "#ROUTER":
		is_reading_networks	= False
	if line.strip()[0:1] != "#":
		if is_reading_networks:
			network	= clean_line(line)
			networks.append(tuple(network.split(',')))
		else:
			config_line = clean_line(line)
			routers.append(tuple(config_line.split(',')))

topologia.close()

list_number_of_bits(networks)
print(networks_bits)
print(networks)
print(routers)
print(first_address)
print(address_class)
print(AddrClass.which_class(address_class))


