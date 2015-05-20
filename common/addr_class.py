from enum import Enum

class AddrClass(Enum):
	a = 1
	b = 2
	c = 3
	def which_class(number):
		if number == "8":
			return AddrClass.a
		if number == "16":
			return AddrClass.b
		if number == "24":
			return AddrClass.c
