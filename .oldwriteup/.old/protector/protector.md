# write up protector 
với bài này thì có bufferoverflow nên em chỉ cần overwrite RIP bằng cái gì đó để nó chạy theo ý muốn của em là được, nhưng mà vấn đề là bài có check seccomp nên em phải dùng các syscall được cho phép như này 

![image](https://github.com/antkss/writeUP/assets/88892713/ef4a7c4a-4128-46f9-b104-14a42dda9f32)


đầu tiên em sẽ dùng mprotect để em set full quyền cho vùng nhớ của binary xong em sẽ dùng mprotect để có thể sử dụng shellcode trên các vùng nhớ đó bằng các syscall còn lại 

đầu tiên em sẽ chuẩn bị các gadget để leak libc 

![image](https://github.com/antkss/writeUP/assets/88892713/cab131f8-11a1-4850-bd5e-6b9925ea7050)

 và 

![image](https://github.com/antkss/writeUP/assets/88892713/077f2ca8-471e-4f5d-b9a6-a121e9fc87f0)

tiếp theo là 

![image](https://github.com/antkss/writeUP/assets/88892713/e401ef53-b150-4cd1-a7c5-5b75a29a30fa)


sau đó em ghi lần lượt vào chương trình như này 

![image](https://github.com/antkss/writeUP/assets/88892713/3b1cf3d3-b660-4bf1-978f-39874a782219)

vì chương trình có buffer nên ghi quá là ok 

địa chỉ rbp mà tại đó nó chứa phần dữ liệu cần chạy của lần nhập thứ 2 của read_plt, cụm pop, địa chỉ chứa địa chỉ libc, giá trị của rsi và rdx là bằng null, cuối cùng là printf_plt để in ra địa chỉ libc, khi in ra libc thì nó chạy đến read_plt và cho phép mình nhập các instructions tiếp theo, và cuối cùng là leave_ret để thay đổi rbp đến chỗ chứa các instruction mình đã nhập và chạy nó (địa chỉ rbp mình nhập phải lớn hơn địa chỉ chứa instruction đầu tiên của mình nhập ở read thứ 2 là 0x8 bytes )
- sau khi chạy payload này thì chương trình sẽ leak ra địa chỉ cùng với cho phép mình nhập các instruction tiếp theo, em sẽ tính toán các gadget cần thiết

![image](https://github.com/antkss/writeUP/assets/88892713/bafb98f2-6013-4ea1-9626-d2404864918c)


- sau đó em sẽ nhập payload như sau

![image](https://github.com/antkss/writeUP/assets/88892713/6b5e4556-dbfc-489c-b8f6-4fc352e3d3d8)

địa chỉ rbp lúc này nó sẽ là địa chỉ đầu tiên, nhưng mà em ko cần chạy instruction nào nữa nên em sẽ để trống, tiếp theo là bộ syscall để set quyền cho các vùng nhớ của binary, em set full vùng nhớ full quyền nên sẽ chạy 5 cái 
tiếp theo là địa chỉ shellcode và cuối cùng là shellcode em nhập vào, vì do ảnh hưởng của syscall nên em sẽ path thêm 6byte để payload có thể chạy liên tục

shellcode em sẽ dùng getdents, open và write để đọc nội dung các thư mục, cách viết shellcode thì quá ok r =))

![image](https://github.com/antkss/writeUP/assets/88892713/b7b9eb43-4dc3-4ae4-b803-7bb3fbe71016)

và cứ thế chương trình chạy lần lượt như vậy


khi chạy thì kết quả nó ra xấu và có chèn thêm các ký tự vớ vẩn nên em xử lý thêm  1 xíu

![image](https://github.com/antkss/writeUP/assets/88892713/d2d0ceec-ccc6-4e29-93bc-1f11ba5aa8e8)


 Kết quả in ra đẹp rồi 

 ![image](https://github.com/antkss/writeUP/assets/88892713/111041a5-90e5-4ffe-ad0b-52e3e79a049f)


 có 1 số cái tên files bị dính ký tự khác vô nhưng vẫn là ký tự in được nên kích thước nó không đảm bảo 16 bytes như trong script nên em để đó tính sau, em lọc ra những tên đảm bảo kích thước trước và dùng

![image](https://github.com/antkss/writeUP/assets/88892713/67fbaf12-1757-4f1a-b96e-7a3817b223c5)

- em ljust sao cho tên thư mục đủ 16bytes để nhập vào vùng địa chỉ binary khá là rộng, xong em open từng files để tìm flag, em sẽ tạo 1 file mới để tìm flag


![image](https://github.com/antkss/writeUP/assets/88892713/da3526c6-eb0d-4bb9-be87-ce67cb4f8634)
em sẽ nhập đống ở trên vào (ở biến folder) rồi chạy cái sycall open trước i chạy từ 0 đến 256 () nhân với khoảng cách từng cái địa chỉ chứa chuỗi đường dẫn cùng với địa chị cái đầu tiên, nó sẽ duyệt hết từng đường dẫn một, các đường dẫn nằm cách đều 

![image](https://github.com/antkss/writeUP/assets/88892713/881fa5f1-8674-4eef-ab07-764805a0eeac)

sau khi open thì em chạy syscall của read và write là có thể in ra

![image](https://github.com/antkss/writeUP/assets/88892713/912a1045-bb02-4df2-a0af-59c0aaf1e2fc)


vì là server nên nó chạy lâu nên em ko chạy nữa =), nhưng mà khả năng tìm ra flag vẫn được =)) vì em chạy thử thấy nó dò từng file một rất ngon =))
