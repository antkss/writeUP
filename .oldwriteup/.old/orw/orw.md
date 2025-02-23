# orw write up 

- với bài này thì chỉ cần truyền shell code vào là nó chạy, nhưng mà vấn đề là bài này có chứa seccomp nên vấn đề truyền shellcode sẽ khó khăn hơn,như seccomp-tools đã trả về kết quả là như sau

![image](https://github.com/antkss/writeUP/assets/88892713/9aba7444-cc10-4ff6-9a32-ad55f7fbb8ca)


 những syscall goto 0x11 sẽ là allow, còn lại là return error, vì vậy em sẽ dùng các syscall mà nó cho phép sử dụng để leak dữ liệu: open, read. write

![image](https://github.com/antkss/writeUP/assets/88892713/9200eb56-d1cd-4cb8-922c-ceb7d9438ab8)
- em sẽ viết scripts như sau để thực hiện truyền shellcode
