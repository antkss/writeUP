# writeup writing on the wall 
- bài này về hành vi so sánh của strcmp, ta thấy rằng giới hạn của array của buff là 6 nhưng ta đươc nhập 7 vì vậy khi tràn null byte ở byte thứ 7 của chuỗi 1 vào chuỗi 2 thì khi so sánh nó sẽ trả về kết quả ngay khi nó so sánh bytes đầu tiên
- vì vậy strcmp sẽ trả về 0
- sau khi nó so sánh thì nó sẽ tự pass qua và lấy được flag
```bash
     0x55555555559e <main+63>    lea    rdx, [rbp - 0x10]
   0x5555555555a2 <main+67>    lea    rax, [rbp - 0x16]
   0x5555555555a6 <main+71>    mov    rsi, rdx
   0x5555555555a9 <main+74>    mov    rdi, rax
 ► 0x5555555555ac <main+77>    call   strcmp@plt                <strcmp@plt>
        s1: 0x7fffffffe63a ◂— 0x3300736170743300
        s2: 0x7fffffffe640 ◂— 0x2073736170743300
 
   0x5555555555b1 <main+82>    test   eax, eax
   0x5555555555b3 <main+84>    jne    main+98                <main+98>
 
   0x5555555555b5 <main+86>    mov    eax, 0
   0x5555555555ba <main+91>    call   open_door                <open_door>
 
   0x5555555555bf <main+96>    jmp    main+113                <main+113>
 
   0x5555555555c1 <main+98>    lea    rax, [rip + 0xb98]
   ```
