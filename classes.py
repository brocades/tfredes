__author__ = 'Gabriel Rubin'

class Address:

    #regions:
    m_Add1 = 0
    m_Add2 = 0
    m_Add3 = 0
    m_Add4 = 0

    def __init__(self, address: str):
        addresses = address.strip().split(".")
        self.m_Add1 = int(addresses[0])
        self.m_Add2 = int(addresses[1])
        self.m_Add3 = int(addresses[2])
        self.m_Add4 = int(addresses[3])

    def getOffsetAddress(self, value: int):

        val1 = int(value % 256)
        val2 = int(value / 256)
        val3 = int(val2  / 256)
        val4 = int(val3  / 256)

        address1 = self.m_Add1 + val4
        address2 = self.m_Add2 + val3
        address3 = self.m_Add3 + val2
        address4 = self.m_Add4 + val1

        return Address(str(address1) + "." + str(address2) + "." + str(address3) + "." + str(address4))


    def __str__(self):
        return str(self.m_Add1) + "." + str(self.m_Add2) + "." + str(self.m_Add3) + "." + str(self.m_Add4)

class IPAddress:

    m_address = None
    m_hostBitLength = 0
    m_maskLength = 0

    def __init__(self, address: str, maskLength: int):
        self.m_address = Address(address)
        self.m_maskLength = maskLength
        self.m_hostBitLength = 32 - maskLength

    def getMaxHosts(self):
        return 2 ** self.m_hostBitLength - 2

    def getMask(self):
        if self.m_hostBitLength == 0 : return Address("255.255.255.255")
        if self.m_hostBitLength == 1 : return Address("255.255.255.254")
        if self.m_hostBitLength == 2 : return Address("255.255.255.252")
        if self.m_hostBitLength == 3 : return Address("255.255.255.248")
        if self.m_hostBitLength == 4 : return Address("255.255.255.240")
        if self.m_hostBitLength == 5 : return Address("255.255.255.224")
        if self.m_hostBitLength == 6 : return Address("255.255.255.192")
        if self.m_hostBitLength == 7 : return Address("255.255.255.128")
        if self.m_hostBitLength == 8 : return Address("255.255.255.0")
        if self.m_hostBitLength == 9 : return Address("255.255.254.0")
        if self.m_hostBitLength == 10: return Address("255.255.252.0")
        if self.m_hostBitLength == 11: return Address("255.255.248.0")
        if self.m_hostBitLength == 12: return Address("255.255.240.0")
        if self.m_hostBitLength == 13: return Address("255.255.224.0")
        if self.m_hostBitLength == 14: return Address("255.255.192.0")
        if self.m_hostBitLength == 15: return Address("255.255.128.0")
        if self.m_hostBitLength == 16: return Address("255.255.0.0")
        if self.m_hostBitLength == 17: return Address("255.254.0.0")
        if self.m_hostBitLength == 18: return Address("255.252.0.0")
        if self.m_hostBitLength == 19: return Address("255.248.0.0")
        if self.m_hostBitLength == 20: return Address("255.240.0.0")
        if self.m_hostBitLength == 21: return Address("255.224.0.0")
        if self.m_hostBitLength == 22: return Address("255.192.0.0")
        if self.m_hostBitLength == 23: return Address("255.128.0.0")
        if self.m_hostBitLength == 24: return Address("255.0.0.0")

    def divide(self):
        childAddress1 = IPAddress(str(self.m_address), self.m_maskLength + 1)
        #print(childAddress1.getMaxHosts() + 2)
        childAddress2 = IPAddress(str(self.m_address.getOffsetAddress(childAddress1.getMaxHosts() + 2)), self.m_maskLength + 1)

        IPs = [childAddress1, childAddress2]
        return IPs

    def __str__(self):
        return ("Address: " + str(self.m_address) + "\n" +
                "Mask: " + str(self.getMask()) + "\n" +
                "HostBitLength: " + str(self.m_hostBitLength) + "\n" +
                "MaskLength: " + str(self.m_maskLength))

class NetworkAlloc:

    m_networks = []

    def getNetworksIPs(self, networks, baseIP):
        self.m_networks = []
        networks.sort()
        networks.reverse()
        self.divideAndAlloc(networks, baseIP, 0)
        return self.m_networks

    def divideAndAlloc(self, networks, currentIP, index: int):
        #Sort by bigger network need to the lesser

        if not networks:
            return False

        if networks[0].m_numNodes <= currentIP.getMaxHosts():
            nextIPs = currentIP.divide()
            if self.divideAndAlloc(networks, nextIPs[0], index) is False:
                if not networks:
                    return False
                networks[0].setIP(currentIP)
                self.m_networks.append(networks[0])
                return True
            else:
                networks.pop(0)
                return self.divideAndAlloc(networks, nextIPs[1], index + 1)

        return False

class Network:

    m_name = ""
    m_numNodes = 0
    m_index = 0

    m_ipAddress = None
    m_addressRangeStart = None
    m_addressRangeFinish = None

    def __init__(self, name: str, numNodes: int, index: int):
        self.m_name = name
        self.m_numNodes = numNodes
        self.m_index = index

    def setIP(self, ipAddress: IPAddress):
        self.m_ipAddress = ipAddress
        self.m_addressRangeStart = ipAddress.m_address.getOffsetAddress(1);
        self.m_addressRangeFinish = ipAddress.m_address.getOffsetAddress(self.m_numNodes)

    def getResultStr(self):
        return (self.m_name + ", " +
                str(self.m_ipAddress.m_address) + ", " +
                str(self.m_ipAddress.getMask()) + ", " +
                str(self.m_addressRangeStart) + "-" +
                str(self.m_addressRangeFinish))

    def getRouterStr(self):
        return (str(self.m_addressRangeStart) + ", " +
                str(self.m_ipAddress.getMask()))

    def __str__(self):
        return ("Name: " + self.m_name + "\n" +
                "Number of Hosts: " + str(self.m_numNodes) + "\n" +
                "IP: " + str(self.m_ipAddress) + "\n" +
                "Address Start: " + str(self.m_addressRangeStart) + "\n" +
                "Address Finish: " + str(self.m_addressRangeFinish))

    def __lt__(self, other):
        return self.m_numNodes.__lt__(other.m_numNodes)

    def __le__(self, other):
        return self.m_numNodes.__le__(other.m_numNodes)

    def __gt__(self, other):
        return self.m_numNodes.__gt__(other.m_numNodes)

    def __ge__(self, other):
        return self.m_numNodes.__ge__(other.m_numNodes)

class Router:

    m_name = ""
    m_numPorts = 0
    m_networkNames = []
    m_networks = []

    def __init__(self, name: str, numPorts: int):
        self.m_name = name
        self.m_numPorts = numPorts

    def getNetworks(self, networks):
        for network in networks:
            if network.m_name in self.m_networkNames:
                self.addNetwork(network)

    def addNetwork(self, network: Network):
        self.m_networks.append(network)

    def getResultStr(self):
        strResult = (self.m_name + ", " +
                     str(self.m_numPorts) + ", ")

        strNetworks = ""

        start = 0

        for network in self.m_networks:
            if start > 0:
                strNetworks += ", "
            strNetworks += network.getRouterStr()
            start += 1

        return strResult + strNetworks

    def __str__(self):
        strResult =  ("Name: " + self.m_name + "\n" +
                        "Ports: " + str(self.m_numPorts) + "\n")
        strNetworks = ""
        i = 1

        for network in self.m_networks:
            strNetworks += "Network " + str(i) + ": " + str(network) + "\n"
            i += 1

        return strResult + strNetw