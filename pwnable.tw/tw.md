# write up tw
### apple store
- với bài apple store vì dữ liệu của sản phẩm iphone 8 để dưới stack nhưng cái đáng quan tâm là hàm handle thực hiện mọi cuộc gọi đến các hàm khác nên các hàm khác đều có chung 1 frame stack
- bài sử dụng double linked list để chứa liên kết dữ liệu nên vì thế thay đổi fd và bk pointer của sản phẩm kia vì bài cho size read cũng hợp lý
- chỉ cần đáp ứng đủ số tiền mua hàng là có thể add iphone 8 
- sau đó có thể sửa fd với bk pointer để ghi đè mọi thứ, từ iphone 8 dạng struct, thông qua đó cũng leak được 1 số địa chỉ nếu ghi đè vào 
- vì thế khi thay đổi có thể thay đổi ebp để từ đó khi return về hàm handler thì có thể thông qua hàm read ngay đầu để read vào system đồng thời /bin/sh vào got
```assembly
   0x08048c05 <+50>:	lea    eax,[ebp-0x22]
   0x08048c08 <+53>:	mov    DWORD PTR [esp],eax
   0x08048c0b <+56>:	call   0x8048799 <my_read>
   0x08048c10 <+61>:	lea    eax,[ebp-0x22]
   0x08048c13 <+64>:	mov    DWORD PTR [esp],eax
   0x08048c16 <+67>:	call   0x8048560 <atoi@plt>
```
- ebp là sẽ là &atoi + 0x22
- shell
```shell
$ ls
applestore        applestoree      cac          libc.so.6
applestore.adb        applestoree.bndb  ld-2.23.so  libc_32.so.6
applestore.adb-journal    break          libc          solve.py
$  
```
### tcache tear
- bài có double free nên có thể malloc ở bất kỳ chỗ nào thỏa mãn điều kiện
- em sẽ fake chunk sao cho nó phù hợp sau đó malloc vào đó luôn
- đầu tiên em cần fake 1 cái chunk cực lớn xung quanh là mấy cái chunk nhỏ để tránh bị check, chunk lớn sao cho đủ để khi free xuống đc unsorted bin để leak địa chỉ libc 
```shell
unsortedbin
all: 0x602050 —▸ 0x7ff1c17ebca0 ◂— 0x602050 /* 'P `' */
smallbins
empty
largebins
```
- tiếp theo sau khi có libc thì malloc vào malloc_hook để đổi thành system, vậy là xong
- lấy được shell
```shell
a.c                          solve.py
a.oute                          tcache_tear
ld-2.27.so                      tcache_teare
libc-18292bd12d37bfaf58e8dded9db7f1f5da1192cb.so  tcache_teare.adb
libc.so.6                      tcache_teare.adb-journal
libc.so.6.adb
$  
```
### house of botcake 
- với kỹ thuật này thì cần malloc 7 chunk có kích thước bằng nhau và thêm 2 chunk nữa là thứ 8 và thứ 9 để merge vào nhau trong unsorted bin, thêm nữa là 1 chunk để ngăn cách với wilderness để tránh bị merge
- tiếp theo là free 7 chunk và 2 chunk cuối, 2 chunk cuối sẽ được merge vào nhau trong unsorted bin
- tại đây có thể leak libc nếu muốn
- tiếp theo là phần để làm cho các chunk bị overlap
- malloc 1 chunk trong 7 chunk trên bị free, free chunk thứ 9 đang trong unsorted bin, để ý chunk thứ 9 đã bị free, nhưng lại bị merge nên chunk lớn đè lên chunk nhỏ dẫn tới overlap
chunk nhỏ sẽ bị chunk lớn sửa đổi fd hoặc bk
- ví dụ với bài house of botcake 

