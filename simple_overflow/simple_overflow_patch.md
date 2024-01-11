### Write up simple_overflow
- đầu tiên để làm được bài overflow thì cần phải xác định không thể gọi shell từ các gadget của binary 
- mục đích của bài là gọi shell bằng cách đổi frame của chương trình thông qua fake rbp, từ đó rsp bị thay đổi theo

### khai thác
- đầu tiên em sẽ overwrite 64 bytes để đến được rbp sau đó em sẽ tìm 1 địa chỉ rbp có rw thay thế có địa chỉ tĩnh 


![image](https://github.com/antkss/writeUP/assets/88892713/0e6cc2b6-7a98-414a-901d-d1c0d77a346e)


- vùng này có vẻ ok
- tiếp theo em sẽ bỏ nó vào rbp rồi ghi địa chỉ của save_data vào để save_data lặp lại 1 lần nữa 
