### Write up simple_overflow
- đầu tiên để làm được bài overflow thì cần phải xác định không thể gọi shell từ các gadget của binary 
- mục đích của bài là gọi shell bằng cách đổi frame của chương trình thông qua fake rbp, từ đó rsp bị thay đổi theo

### khai thác
## lần lặp 1 của save_data
- đầu tiên em sẽ overwrite 64 bytes để đến được rbp sau đó em sẽ tìm 1 địa chỉ rbp có rw thay thế có địa chỉ tĩnh


![image](https://github.com/antkss/writeUP/assets/88892713/0e6cc2b6-7a98-414a-901d-d1c0d77a346e)


- vùng này có vẻ ok, vậy em lấy địa chỉ rbp từ 0x0000000000404308
- tiếp theo em sẽ bỏ nó vào rbp rồi ghi địa chỉ của save_data theo sau rbp để sau khi return thì chương trình vào để save_data lặp lại 1 lần nữa 
- vậy lần 1 ghi sẽ có được như sau:

  ![image](https://github.com/antkss/writeUP/assets/88892713/7c5ceb87-ee0d-49e7-89b6-fa834c1a363e)


## tiếp theo là đến lần lặp thứ 2 của save_data
- địa chỉ ghi dữ liệu của read đã bị thay đổi, vậy là thành công thay đổi frame

![image](https://github.com/antkss/writeUP/assets/88892713/915adc3d-2796-4262-a2eb-ee6dca30bb1e)


- lần này em sẽ ghi lại lần nữa địa chỉ save_data ở lần ghi 1 để nó tự quay lại save_data và em lưu lại địa chỉ rsp hiện tại để xíu quay lại check
- 0x00000000004042c8
- vậy lần ghi 2 sẽ có được như sau:

![image](https://github.com/antkss/writeUP/assets/88892713/d0569064-c2e2-4f73-a979-4d3021fffa97)

## tiếp theo là đến lần lặp thứ 3 của save_data
- lần nhập này 



