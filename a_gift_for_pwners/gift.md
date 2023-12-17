### Write up a gift for pwners
 Đầu tiên mở ida lên ta thấy 
```c++
 if ( !strncmp(s, "KCSC{A_gift_", 0xCuLL) )
    printf("The second part of the flag I hide somewhere in some function");
  return 0;
```
Phần thứ 2 ở:
```c++
int secret()
{
  puts("for_the_");
  return printf("The last part is somewhere in the file but I don't remember =)))");
}
```
và cuối cùng, sử dụng lệnh strings gift để lấy chuỗi đọc được 
```c++
Guest the flag:
KCSC{A_gift_
The second part of the flag I hide somewhere in some function
;*3$"
pwners_0xdeadbeef}
GCC: (Debian 13.2.0-4) 13.2.0
Scrt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
```
- Ghép 3 mảnh ghép lại: 
KCSC{A_gift_for_the_pwners_0xdeadbeef}
