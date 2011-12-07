#!/usr/bin/python

import sys
import re

# Load file argument contents into a single string
f = open(sys.argv[1])
contents = f.read()
f.close()

# Strip C-style comments, taken from http://stackoverflow.com/a/241506
def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

nocomment = comment_remover(contents)

# Extract module declaration as section between module keyword and semicolon
moduledec = nocomment.split('module')[1].split(';')[0]

# Module name is prior to bracket
module_name = moduledec.split('(')[0].strip()
print 'Module Name: ' + module_name

# Module ports are section within brackets, separated by comma
# Remove whitespace and strip reg from output declaration
module_ports = moduledec.split('(')[1].split(')')[0].split(',')
ports = [a.strip().replace(' reg ',' ').replace(' wire ',' ') for a in module_ports]
# print ports

# Remove superfluous spaces in port index
ports_a = [re.sub(r'\[\s*(\d+)\s*:\s*?(\d+)\s*\]\s*(.)', r'[\1:\2] \3', a) for a in ports]

# Construct a list of tuples for input and output ports
# Each tuple is the port name, width, MSB index, LSB index
in_ports = []
out_ports= []
inout_ports= []
for a in ports_a:
	a_split= a.split()
	# print a_split
	if len(a_split) == 3:
		# Extract two numbers separated by colon surrounded by square brackets
		bits = [int(x) for x in a_split[1].split('[')[1].split(']')[0].split(':')]
		bit_width = abs(bits[0]-bits[1])+1
	else:
		bit_width = 1
		bits = [0,0]
	
	port_tuple = (a_split[-1], bit_width, bits[0], bits[1])

	if a_split[0] == 'input':
		in_ports.append(port_tuple)
	elif a_split[0] == 'output':
		out_ports.append(port_tuple)
	elif a_split[0] == 'inout':
		inout_ports.append(port_tuple)

print 'Inputs (name, width, msb, lsb):\n' + str(in_ports)
print 'Outputs: (name, width, msb, lsb):\n' + str(out_ports)
if len(inout_ports) > 0:
	print 'InOuts: (name, width, msb, lsb):\n' + str(inout_ports)
