# write up ulele
- bài cơ bản bị lỗi ép kiểu
```cpp
igned __int64 __fastcall sub_1747(__int64 a1)
{
  int v2; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  std::operator<<<std::char_traits<char>>(&std::cout, "Enter the index of the note to destroy: ");
  std::istream::operator>>(&std::cin, &v2);
  if ( v2 < 0 )
    exit(1);
  sub_1BF8(a1, (unsigned __int8)v2);
  *(_QWORD *)sub_207A(a1, v2) = 0LL;
  return v3 - __readfsqword(0x28u);
}
```
- hàm này nằm trong option 3 của chương trình, v5 là biến ta nhập vào, nhưng khi đi vào hàm sub_1BF8 thì ép thành kiểu unsigned __int8
- trong hàm sub_1BF8 thì hàm sử dụng operator delete để free con trỏ heap, giả sử index là 0x100 thì nó sẽ chỉ lấy 0x00 làm index còn 0x01 thì sẽ bị bỏ, vì vậy index bị free sẽ là 0
  ```cpp
  void __fastcall sub_1BF8(_QWORD *a1, unsigned __int8 a2)
{
  void *v3; // rax

  if ( a2 >= (unsigned __int64)sub_2052(a1) || !*(_QWORD *)sub_207A(a1, a2) )
  {
    std::operator<<<std::char_traits<char>>(&std::cerr, "Note index out of range.");
    std::ostream::operator<<();
    exit(1);
  }
  v3 = **(void ***)sub_207A(a1, a2);
  if ( v3 )
    operator delete(v3, 1uLL);
}
  ```
- đến phần nó xóa con trỏ, con trỏ bị xóa sẽ vẫn lấy 0x100, vậy thì uaf đã được kích hoạt
```cpp
 *(_QWORD *)sub_207A(a1, v2) = 0LL;
 ```
- - sau khi có uaf, tiếp theo để có double free, ta có thể double free bằng cách đẩy xuống fastbin, vì chương trình cho size không thể tùy chình
--  sau khi có được control với fd thì ta có thể control được kích thước của các chunk khác, từ đó có thể overwrite size và leak libc, còn leak heap thì có thể dùng uaf
- chương trình cũng có hàm để in ra nội dung nên có thể dùng để leak
- sau khi có được libc thì có thể leak stack bằng việc sử dụng environ và cuối cùng là overwrite rip của 1 hàm nào đó sau đó là getshell, bài cho kích thước khá ổn nên chỉ cần malloc lần tiếp theo và overwrite rip 1 lần và return của hàm add là có thể get-shell
- ```bash
[*] Switching to interactive mode
 $ ls
Dockerfile            libc.tar        ulele       ulele.id2  ulelee.i64
a.py                  libgcc_s.so.1   ulele.bndb  ulele.md
ld-linux-x86-64.so.2  libm.so.6       ulele.i64   ulele.nam
libc                  libstdc++.so.6  ulele.id0   ulele.til
libc.so.6             solve           ulele.id1   ulelee
$  
```

