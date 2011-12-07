#About#
This respository will hold a series of tools for procesing Verilog files, all written in Python.

##vmodule.py##
Usage:
`./vmodule.py filename.v`

This script extracts the module declaration from the Verilog file, outputs the modules name, and a list of input and output ports (and inout ports if present), each item being a tuple of port name, port width, most significant bit index, least significant bit index.

Known Limitations:

- The script will not process files with more than one module
- It only understands Verilog-2001 module declarations (with the directions and widths within the brackets)

