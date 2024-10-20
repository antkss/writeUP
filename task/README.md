# writeup steg 
- đây là 1 challenge thực tế liên quan đến buffer overflow của 1 tool được sử dụng để ẩn dấu thông tin bí mật trong hình ảnh dạng .png hoặc .bmp
- bài cung cấp cho mình 2 file là file đã fix tên steghide_patched và file chưa fix bug tên là steghide, khi dùng bindiff có thể dễ dàng phát hiện ra phần mà hàm đã được vá lỗi
-
![image](https://github.com/user-attachments/assets/8bf1d0a4-421e-449b-a143-cba30b179b7b)


- có thể thấy rằng hàm đã được sửa duy nhất dấu >= thành >
```c
  for ( i = 0LL; i <= height; ++i )
  {
    for ( j = 0LL; j < linelength; ++j )
    {
      BinIO = (BinaryIO *)CvrStgFile::getBinIO(this);
      v2 = (_BYTE *)std::vector<unsigned char>::operator[]((_QWORD *)this + 21, j + i * linelength);
      *v2 = BinaryIO::read8(BinIO);
      ++numread;
    }
```
- vì numread được cộng giá trị vào qua mỗi lần lặp của linelength nên khi height được thêm 1 đơn vị đồng nghĩa với việc numread được thêm vào linelength-1 đơn vị nữa do đó khi qua hàm này sử dụng numread làm số bytes copy cho memcpy
 ```c
void *__fastcall getheaders(unsigned __int8 *a1)
{
  void *v1; // rsp
  __int64 v3; // [rsp+0h] [rbp-30h] BYREF
  void *src; // [rsp+8h] [rbp-28h]
  void *dest; // [rsp+10h] [rbp-20h]
  __int64 v6; // [rsp+18h] [rbp-18h]

  src = a1;
  v6 = height * linelength - 1;
  v1 = alloca(16 * ((height * linelength + 15) / 0x10uLL));
  dest = &v3;
  return memcpy(&v3, a1, numread);
}
```
- sẽ xảy ra overflow
- trong khi pie tĩnh nên ta có rất nhiều gadgets
- ta có thể upload lên 1 file ảnh có chứa gadgets, gadgets phải được bỏ vào file theo đúng offset và từ đó có thể chiếm được shell

![image](https://github.com/user-attachments/assets/969f1452-eee4-4471-84d5-d8e790f35ece)

- về cơ bản chall tạo ra 1  trang web có cho phép upload file ảnh để dấu thông tin vào file

![image](https://github.com/user-attachments/assets/f6456705-2ba6-4553-94ec-8f417fea1ab9)

- wrapper được code python và thực thi command

  `````
