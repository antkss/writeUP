#!/usr/bin/env python3
import pwn

exe = pwn.ELF("./super-luckye")
pwn.context.log_level='debug'
pwn.context.terminal = ["foot"]
p = pwn.gdb.debug([exe.path],"""

                """)
if pwn.args.REMOTE:
    p = pwn.remote("addr", 1337)

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)


if __name__ == "__main__":
    # p = conn()







    # good luck pwning :)
    p.interactive()
