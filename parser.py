import sys

filename = sys.argv[1]
topologia = open(filename, 'r')
networks = []
routers = []
is_reading_networks = True

# Parses networks and routers
for line in topologia.readlines():
	if line[0:2] == "#R":
		is_reading_networks	= False
	if line[0:1] != "#":
		if is_reading_networks:
			network	= line.split(',')
			net_name = network[0].strip()
			num_nodes = network[1].strip()
			networks.append(tuple([net_name,num_nodes]))
		else:
			config_line	= tuple(line.split(','))
			#<router_name>, <num_ports>, <(net|router)_name0>, <(net|router)_name1>, …, <(net|router)_nameN>
			router_parameters = []
			for parameter in config_line:
				router_parameters.append(parameter.strip())
			routers.append(tuple(router_parameters))

topologia.close()

for network	in networks:
	print(network)
for router	in routers:
	print(router)