# write UP info store 
- với bài này em thấy rằng ở tại đây có formatstring nên em sẽ leak được địa chỉ từ đây, à còn nữa là cái stack thực thi được nên em sẽ leak stack luôn sau đó e ghi shellcode vào và ghi địa chỉ shellcode vào rip là có thể chạy shellcode


![image](https://github.com/antkss/writeUP/assets/88892713/bea166ff-0469-41ec-b19c-d624c36c8e0f)



![image](https://github.com/antkss/writeUP/assets/88892713/b08f18de-5878-41ce-a34b-ccf24fbd060f)

- nhưng mà mình chỉ nhập được có 10 ký tự, khả năng có thể leak được 2 thứ cùng lúc

![image](https://github.com/antkss/writeUP/assets/88892713/b965cc0a-9e2e-467a-bd82-32a0904849c3)

- breakpoint đến đoạn printf thì sẽ thấy rằng rdi có 1 cái địa chỉ ở trên nên em sẽ leak địa chỉ này luôn, tham số đầu tiên nên format string ngắn gọn tiết kiệm diện tích 
- tiếp theo là leak canary ở vị trí này

![image](https://github.com/antkss/writeUP/assets/88892713/afb2ba4c-efc0-4fad-bc97-1972d6bf9039)


- ở code em thấy rằng có buffer overflow

![image](https://github.com/antkss/writeUP/assets/88892713/c85584e7-e8e6-43b4-aded-a88ef8c4e67c)


- nên em sẽ ghi shellcode để chạy

vậy là xong, shellcode em sẽ ghi sau rip vì mấy cái hàm này khi chạy nó sẽ xóa shellcode khi shellcode nằm ở vùng rsp -> rbp 

![image](https://github.com/antkss/writeUP/assets/88892713/441e563c-1994-4d04-8527-ee6b1da8544b)


- em sẽ tính offset đến canary, ghi canary tại đó và tíếp theo là đến rip, ghi địa chỉ shellcode vào và cuối cùng là shellcode em sẽ ghi sau cùng


![image](https://github.com/antkss/writeUP/assets/88892713/eacc60c0-8948-45b5-a643-d4b04b806632)


- vậy là truy cập được shell rồi 

![image](https://github.com/antkss/writeUP/assets/88892713/95fb1b62-c111-482f-a97b-dd4650b90169)
