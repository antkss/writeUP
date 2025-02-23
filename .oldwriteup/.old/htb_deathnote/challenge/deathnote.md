# write up deathnote 
- bài này chủ yếu là leak libc, còn lại là hàm backdoor làm việc còn lại
- em sẽ allocate 8 chunk và 1 chunk thứ 9 nhỏ để tránh bị đọng vào topchunk, sau đó free 8 chunk, rồi nhờ uaf để leak libc, lúc này xuất hiện chunk dưới unsorted bin
```bash
pwndbg> bin
tcachebins
0x90 [  7]: 0x55555555aa10 —▸ 0x55555555a980 —▸ 0x55555555a8f0 —▸ 0x55555555a860 —▸ 0x55555555a7d0 —▸ 0x55555555a740 —▸ 0x55555555a6b0 ◂— 0
0x410 [  1]: 0x55555555a2a0 ◂— 0
fastbins
empty
unsortedbin
all: 0x55555555aa90 —▸ 0x55555541ace0 ◂— 0x55555555aa90
smallbins
empty
largebins
empty
```
```c
    puts(aExecuting);
    v2(*(_QWORD *)(a1 + 8));
````
- hàm backdoor sẽ thực thi code địa chỉ từ vùng heap mà ta nhập vào
