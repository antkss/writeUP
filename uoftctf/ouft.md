# Nothing to return 
- với bài này có buffer overflow, em cần lấy địa chỉ libc ra để kiếm gadget tạo shell vì nó ko có hàm tạo shell có sẵn, địa chỉ đã được chương trình cung cấp thông qua format string

![image](https://github.com/antkss/writeUP/assets/88892713/493d77c3-7cb4-4cac-b4d5-96fddd71c0d1)


sau khi lấy đc địa chỉ thì tính toán các địa chỉ base rồi tìm địa chỉ của các gadget cần thiết như system, chuỗi /bin/sh, pop_rdi

![image](https://github.com/antkss/writeUP/assets/88892713/2145930e-2299-4278-805a-46cfcd446e5f)

offset đến dược saved rip là 72 


![image](https://github.com/antkss/writeUP/assets/88892713/b26dd36d-4182-4750-ad90-6cc1746c2379)

ở đây e bỏ thêm địa chỉ của return vì để tránh lẻ stack

ok vậy là thành công chạy shell 


![image](https://github.com/antkss/writeUP/assets/88892713/f1bc098f-f85c-44c6-bbfa-4bd40c8a81dd)



### với bài patched shell và bài basic overflow thì tương đối giống nhau nên mình chỉ cần tính offset và để dịa chỉ save rip là hàm win là ok
### với bài shellcode thì mình chỉ cần viết đúng shellcode và input trực tiếp vô chương trình là  ok 
