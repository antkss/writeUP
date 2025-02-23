#!/bin/python
from pwn import *
exe = ELF('./')
libc = ELF("./libc-2.23.so")
ld = ELF("./ld-2.23.so")
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''


           ''')
#################exploiting#####################
p.sendline(payload)
##############the end###########################
p.interactive()
