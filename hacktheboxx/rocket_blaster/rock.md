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

