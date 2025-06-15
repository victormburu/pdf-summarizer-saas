#!/usr/bin/env python
def faulty_read_and_divide(filename):
	with open(filename, 'r') as file:
		data = file.readlines()
		num1 = int(data[0])
		num2 = int(data[1])
		return num1 / num2
