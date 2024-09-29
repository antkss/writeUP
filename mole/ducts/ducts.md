# write up ducts 
- bài bao gồm có hàm talk dùng để tương tác chính và 1 hàm backend, hàm backend nhận buffer từ hàm talk, hàm talk sử dụng fork() để có thể listen được nhiều connection cùng 1 lúc, nhưng tuy nhiên sử dụng chung 1 pipe nên gây ra lỗi
- backend cũng dùng chung 1 pipe[0] read
```c
  pipe(pipedes);
  if ( !fork() )
    backend((unsigned int)pipedes[0], argv);
```

```c
     break;
    if ( !fork() )
      talk(v9, (unsigned int)pipedes[1]);
  }
  close(fd);
```
- ta sẽ có 1 hàm duy nhất để gửi dữ liệu tới backend thông qua 1 pipe duy nhất
```c
ssize_t __fastcall send_message(_DWORD *a1, int fd)
{
  return write(fd, a1, a1[1] + 80);
}
```
