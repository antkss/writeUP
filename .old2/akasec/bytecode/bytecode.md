# write up bytecode 
- đọc code thấy rằng bài check khá cẩu thả như thế này 
```c

if ((unpack(code + i, sizeof(int)) & 0xffffff00) == 
        ( (uint64_t)(stack) & 0xffffff00)
        && (unpack(code + i, sizeof(int)) < (stack + STACK_SIZE))){
        ....
 }
```
- về cơ bản thì nó chỉ check lấy 3 bytes địa chỉ đầu của địa chỉ được truyền vào để so sánh với 3 bytes địa chỉ stack, nếu nó khác thì không cho run nội dung bên trong
```assembly
pwndbg> tel 0x404000
00:0000│  0x404000 (data_start) ◂— 0
01:0008│  0x404008 (__dso_handle) ◂— 0
02:0010│  0x404010 ◂— 0
03:0018│  0x404018 ◂— 0
04:0020│  0x404020 (stdout@GLIBC_2.2.5) —▸ 0x7ffff7f915c0 (_IO_2_1_stdout_) ◂— 0xfbad2887
05:0028│  0x404028 ◂— 0
06:0030│  0x404030 (stdin@GLIBC_2.2.5) —▸ 0x7ffff7f908e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
07:0038│  0x404038 ◂— 0
pwndbg> 
08:0040│  0x404040 (stderr@GLIBC_2.2.5) —▸ 0x7ffff7f914e0 (_IO_2_1_stderr_) ◂— 0xfbad2087
09:0048│  0x404048 ◂— 0
0a:0050│  0x404050 ◂— 0
0b:0058│  0x404058 ◂— 0
0c:0060│  0x404060 (stack) ◂— 0
0d:0068│  0x404068 (stack+8) ◂— 0
0e:0070│  0x404070 (stack+16) ◂— 0
0f:0078│  0x404078 (stack+24) ◂— 0
pwndbg> 

```
- nhưng mà vì vùng của những địa chỉ này chứa stdin, out, err thỏa mãn nên ta có thể leak libc thông qua puts
- ngoài ra chương trình trang bị thêm phần copy dữ liệu nên có thể dễ dàng ghi đè stdout, sau khi fake xong thì chương trình có thêm hàm fwrite để có thể run được fake stdout 
- ta sẽ cần dùng đến LEA, PUTS, và PTR
- sau 77 49 test case thì em đã tìm ra 1 path để call gadgets
```c
call fwrite-> call puts-> return vtable-> call _IO_wfile_seekoff-> call __GI__IO_switch_to_wget_mode
```
```c
Dump of assembler code for function __GI__IO_switch_to_wget_mode:
   0x00007ffff7e58ea0 <+0>:	mov    rax,QWORD PTR [rdi+0xa0]
   0x00007ffff7e58ea7 <+7>:	push   rbx
   0x00007ffff7e58ea8 <+8>:	mov    rbx,rdi
   0x00007ffff7e58eab <+11>:	mov    rdx,QWORD PTR [rax+0x20]
   0x00007ffff7e58eaf <+15>:	cmp    QWORD PTR [rax+0x18],rdx
   0x00007ffff7e58eb3 <+19>:	jae    0x7ffff7e58ed4 <__GI__IO_switch_to_wget_mode+52>
=> 0x00007ffff7e58eb5 <+21>:	mov    rax,QWORD PTR [rax+0xe0]
   0x00007ffff7e58ebc <+28>:	mov    esi,0xffffffff
   0x00007ffff7e58ec1 <+33>:	call   QWORD PTR [rax+0x18]
```
- tại __GI__IO_switch_to_wget_mode sẽ có 1 cái call rất sus và nó call những gì mình có thể kiểm soát từ _IO_FILE_plus fake nên mình có thể chạy gadget từ đây  
- sau khi run script 
```bash
[*] Switching to interactive mode
 sh: line 1: $'\020\b': command not found
$ ls
Dockerfile   bytecode         ld-linux-x86-64.so.2  makefile    sc.py      test
__pycache__  bytecodee.bndb  libc.so.6           message.txt    solve.py
b.py         flag.txt         main.c           need.py    struct.c
$  
```

