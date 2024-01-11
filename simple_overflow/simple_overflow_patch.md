# Write up simple_overflow
- đầu tiên để làm được bài overflow thì cần phải xác định không thể gọi shell từ các gadget của binary
- mục đích của bài là gọi shell bằng cách đổi frame của chương trình thông qua fake rbp, từ đó rsp bị thay đổi theo, sử dụng stack pivoting
## khai thác
#### lần lặp 1 của save_data
- đầu tiên em sẽ overwrite 64 bytes để đến được rbp sau đó em sẽ tìm 1 địa chỉ rbp có rw thay thế có địa chỉ tĩnh


![image](https://github.com/antkss/writeUP/assets/88892713/0e6cc2b6-7a98-414a-901d-d1c0d77a346e)


- vùng này có vẻ ok, vậy em lấy địa chỉ rbp từ 0x0000000000404308
- tiếp theo em sẽ bỏ nó vào rbp rồi ghi địa chỉ của save_data theo sau rbp để sau khi return thì chương trình vào để save_data lặp lại 1 lần nữa 
- vậy lần 1 ghi sẽ có được như sau:

  ![image](https://github.com/antkss/writeUP/assets/88892713/7c5ceb87-ee0d-49e7-89b6-fa834c1a363e)


### tiếp theo là đến lần lặp thứ 2 của save_data
- địa chỉ ghi dữ liệu của read đã bị thay đổi, vậy là thành công thay đổi frame

![image](https://github.com/antkss/writeUP/assets/88892713/915adc3d-2796-4262-a2eb-ee6dca30bb1e)


- lần này em sẽ ghi lại lần nữa địa chỉ save_data ở lần ghi 1 để nó tự quay lại save_data và em lưu lại địa chỉ rsp hiện tại để xíu quay lại check
- 0x00000000004042c8
- vậy lần ghi 2 sẽ có được như sau:

![image](https://github.com/antkss/writeUP/assets/88892713/d0569064-c2e2-4f73-a979-4d3021fffa97)

### tiếp theo là đến lần lặp thứ 3 của save_data
- lần nhập này em sẽ không nhập gì cả mà chỉ nhập fake rbp và địa chỉ để quay lại hàm save_data, vì khi đi qua hàm puts của lần lặp thứ 3, tại địa chỉ 0x404308 (là địa chỉ rbp của lần lặp của save_data thứ 2 được nhập vào từ lần lặp thứ 1) sẽ có địa chỉ cho em leak

- vậy lần ghi thứ 3 là:

![image](https://github.com/antkss/writeUP/assets/88892713/bf00cdec-5cd8-4387-a215-a7a0d4e40a38)



![image](https://github.com/antkss/writeUP/assets/88892713/6faaeb3e-0916-4757-a606-3886a96dffb1)



- khi ta chạy đến hàm puts và thực thi nó, các gía trị rác sẽ được đẩy lên vùng có chứa địa chỉ rbp 0x404308

![image](https://github.com/antkss/writeUP/assets/88892713/eb0802fd-cd26-47b0-9200-e4b2683155ba)

- tại địa chỉ 0x404308 ta có 3 con trỏ trỏ liên tiếp đến nhau như này

  ![image](https://github.com/antkss/writeUP/assets/88892713/b8073dcc-78e7-43bb-84a7-2324a4585b5a)

- và nếu em lấy địa chỉ 0x404308 +0x58 nhập vào payload để đổi thành rbp thì khi chạy thì khi qua vị trí này của lần lặp thứ 4, printf sẽ in ra cái địa chỉ sau cùng 

![image](https://github.com/antkss/writeUP/assets/88892713/d7455c0b-16bc-4d47-92bb-5400a01c5709)

- mov    rax, QWORD PTR [rbp-0x58] : lệnh này mov giá trị của 0x404308 vào rax
- mov    rsi, rax                  : lệnh này mov giá trị của rax vào rsi


### tiếp theo là đến lần lặp thứ 4 của save_data



![image](https://github.com/antkss/writeUP/assets/88892713/688719ff-9731-4fcc-b662-7234799df9ad)

- lệnh printf sẽ in ra địa chỉ này 0x00007f77fd73a2d0, và thế là thành công leak địa chỉ 


![image](https://github.com/antkss/writeUP/assets/88892713/6c1af3f9-fda5-4a3d-87c0-d5eb0a53ceb6)


- em sẽ chọn không ghi gì cả mà đến lần lặp thứ 5 vì nếu e dùng vùng ghi hiện tại hàm system sẽ có trục trặc khi return vì nó nhảy sang vùng read only do cái lệnh "sub rsp,0x388" nên em sẽ đổi vùng sang chỗ khác để đảm bảo nó subtract sang vùng rw 

- vậy lần ghi thứ 4: 

![image](https://github.com/antkss/writeUP/assets/88892713/b0b8b4c0-bf7a-41a3-92d2-0793dff8ac09)


### tiếp theo là đến lần lặp thứ 5 


- tiếp theo em tính toán địa chỉ base libc dựa trên địa chỉ leak được đồng thời tìm địa chỉ của system và chuỗi /bin/sh và pop rdi là em sẽ hoàn thành được 1 shell code, em sẽ làm 1 quả payload như sau: 


![image](https://github.com/antkss/writeUP/assets/88892713/1f3a48cf-7091-4125-bd08-7634f36ff4c3)



- chạy đến read và nhập vào, vậy lần ghi thứ 5 là: 

![image](https://github.com/antkss/writeUP/assets/88892713/c602730b-479b-463e-9639-9a3e1d3bf39a)


### chạy script
 - và cuối cùng thì hoàn thành script
 - cuối cùng là chạy nó thôi

![image](https://github.com/antkss/writeUP/assets/88892713/e2b47e66-ba54-4aee-85e3-251175468650)


