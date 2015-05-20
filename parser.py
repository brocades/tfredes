from common.addr_class import AddrClass
import sys

filename = sys.argv[1]
first_address_type = sys.argv[2]
topologia = open(filename, 'r')
networks = []
routers = []
is_reading_networks = True

# Parse first address and IP class
address_aux = first_address_type.strip().split('/')
first_address = address_aux[0]
address_class = address_aux[1]

# Removes white spaces and line endings
def clean_line(line):
	return line.strip().replace(" ","")

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

print(networks)
print(routers)
print(first_address)
print(address_class)
print(AddrClass.which_class(address_class))


