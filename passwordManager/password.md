# writeup password manager insomnihack
- nếu nhìn vào hàm này em đặt tên là hàm view thì ta có thể thấy rằng có format string, không những có 1 mà có tới 3 vì vậy em có thể sử dụng để leak địa chỉ, ghi địa chỉ các thứ, vì hàm dùng vòng lặp while nữa nên tiện để leak và ghi nhiều lần


![image](https://github.com/antkss/writeUP/assets/88892713/a3ddeb47-43f1-44e7-bd3d-0ac1254e8cfc)


đầu tiên em sẽ chọn option 1 và sau đó nhập tên là format string, password là format string, và URL là format string để leak libc, canary, địa chỉ stack từ rbp, sau khi leak xong thì xử lý 1 chút là có được địa chỉ

![image](https://github.com/antkss/writeUP/assets/88892713/19298dc0-6ac2-42cf-b6bb-61b8b68f7b11)


tiếp theo là tính toán các địa chỉ cần thiết cho bộ gadget pop rdi, system_libc, chũôi /bin/sh từ địa chỉ đã leak được

![image](https://github.com/antkss/writeUP/assets/88892713/196adac3-2779-4a68-b900-4f3b0012e3e5)

bài này có thể dùng format string để ghi nữa nhưng mà em thấy ghi qua buffer overflow nhanh hơn vì ko phải lo đến việc địa chỉ quá lớn để ghi nữa, lỗi buffer từ việc nhập URL ở option 1 

![image](https://github.com/antkss/writeUP/assets/88892713/341261ed-71a0-4c73-8e71-2764e43a4faf)


gets cho phép nhập vô hạn, vì thế em chỉ cần ghi đè vào saved rip là được 

![image](https://github.com/antkss/writeUP/assets/88892713/f0de5cc6-488e-4684-9a71-f496949a95e2)


sau khi ghi em được như vậy, vậy là xong, chạy đến return là có shell


![image](https://github.com/antkss/writeUP/assets/88892713/f65de016-20d1-4edf-a3a7-73dae72e7beb)


![image](https://github.com/antkss/writeUP/assets/88892713/25892c64-14e0-44dc-b6b4-55298638f934)



