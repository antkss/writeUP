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

- vì vậy phương pháp đó là ghi thật nhiều lần vào pipe cùng 1 lúc, lúc đó dữ liệu sẽ bị chồng đè lên nhau khi gửi qua buff bên backend, từ đó ta có thể thực hiện command bên backend,
```c
void backend(undefined4 param_1)
{
  int message_type;
  
  first = NULL_MESSAGE;
  last = NULL_MESSAGE;
  devnull = fopen("/dev/null","w");
  do {
    while (message_type = identify_incoming(param_1), message_type == 1) {
      handle_command(param_1);
    }
    if (((message_type < 2) && (message_type != -1)) && (message_type == 0)) {
      handle_message(param_1);
    }
  } while( true );
}
```
- ta sẽ run cho đến khi nào messege_type ==1 đúng vào buffer mà ta đã gửi đến backend
- lúc đó ta có thể control được command để leak địa chỉ

