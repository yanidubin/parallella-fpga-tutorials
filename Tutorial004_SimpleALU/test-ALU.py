#!/usr/bin/env python2
"""
Example script for driving the Simple ALU example

Written by Yani Dubin (parallellagram.org).
Hereby released into the public domain without restriction.
"""

from mmap import mmap
import struct
from time import sleep

BASE_ADDR=0x60000000  # Base address we locked in when instantiating the PCore
SIZE_ADDR=5*4         # 4K was selected when we instantiated the PCore, but we only need 5 * 32-bit registers

opcodes = {
  'ADD' : 1,
  'SUB' : 2,
  'AND' : 3,
  'MUL' : 4
}

with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), SIZE_ADDR, offset=BASE_ADDR)

def do_operation(opcode, op1, op2, printres=False):
  # First we write the operands, then the opcode
  mem[ 4: 8] = struct.pack("<L", op1)
  mem[ 8:12] = struct.pack("<L", op2)
  mem[ 0: 4] = struct.pack("<L", opcodes[opcode])
  sleep(0.1)

  # Finally we read out the result
  res1 = struct.unpack("<L", mem[12:16])[0]
  res2 = struct.unpack("<L", mem[16:20])[0]

  result = (res2 << 32) + res1

  if printres:
    print("%s(%8d, %8d) -> %d") %(opcode,op1,op2,result)
  return result

# Do a quick test to ensure each operation performs as expected
do_operation('ADD', 11111, 22222, True)
do_operation('SUB', 33333, 22222, True)
do_operation('AND', 0x3232, 0x8222, True)   # Hence result should be 0x222 = 546
do_operation('MUL', 50000000, 200000, True) # Will overflow 32-bits to ensure we have 64-bit result.

# Example of test automation - could extend this to use random values, and test all operations.
for i in range(0, 500):
  for j in range(0, 500):
    res = do_operation('ADD', i, j)
    if res != i+j:
      print "ERROR %d+%d != %d" %(i,j,i+j)
