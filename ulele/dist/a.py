from pwn import * 
for i in range(128):
    p = process("./ulelee") 
    p.sendlineafter(b">",b"2")
    p.sendlineafter(b":",str(i-64).encode())
    data = p.recvall()
    log.info(f"data: {data}")
