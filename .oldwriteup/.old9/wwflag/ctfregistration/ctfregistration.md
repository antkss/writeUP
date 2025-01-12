# ctfregistration
- chương trình dùng heap allocator của 1 dự án trên git, tên là rpmalloc sử dụng singlely linked list để quản lý chunk đã free - https://github.com/mjansson/rpmalloc
- khi tạo 1 chunk, chương trình sẽ cho người dùng nhập thông tin, 8 bytes đầu là old, 0x10 bytes dsau là name và 0x20 bytes sau là nhập des
```c
int register_hacker()
{
  unsigned __int64 i; // [rsp+0h] [rbp-10h]
  hacker *tmp; // [rsp+8h] [rbp-8h]

  for ( i = 0LL; hackers[i]; ++i )
    ;
  if ( i > 0x63 )
    return puts("Sorry ! No spots left :/");
  tmp = (hacker *)rpmalloc(0x30LL);
  printf("How old is the hacker? ");
  scanf("%lu", tmp);
  getchar();
  printf("What's the hacker's name ? ");
  scanf("%16[^\n]s", &tmp->name);
  getchar();
  printf("How would you describe this hacker ? ");
  scanf("%32[^\n]s", &tmp->des);
  getchar();
  hackers[i] = tmp;
  return printf("Your hacker number is %zu !\n", i);
}
- nếu check có thể thấy 0x32 là đủ 4 ô nhớ
```c
00:0000│ rsi 0x555540000120 ◂— 'aaaaaaaa'
01:0008│     0x555540000128 ◂— 0
02:0010│     0x555540000130 ◂— 0
03:0018│     0x555540000138 ◂— 0
04:0020│     0x555540000140 —▸ 0x555540000170 —▸ 0x5555400001a0 —▸ 0x5555400001d0 —▸ 0x555540000200 ◂— ...
```
tuy nhiên scanf thêm NULL byte vào cuối nên khi nhập đủ buffer, null byte sẽ đè lên forward pointer của chunk hiện tại và next chunk lúc này sẽ trở thành 
```
00:0000│  0x555540000120 ◂— 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
01:0008│  0x555540000128 ◂— 'bbbbbbbbbbbbbbbbbbbbbbbb'
02:0010│  0x555540000130 ◂— 'bbbbbbbbbbbbbbbb'
03:0018│  0x555540000138 ◂— 'bbbbbbbb'
04:0020│  0x555540000140 —▸ 0x555540000100
```
- vì vậy khi allocate chunk mới sẽ overlap chunk cũ và khi đó có thể control forward pointer của chunk nằm trên do đó có tể allocate
- khi đó có thể control và leak libc bằng option 2, sau đó có thể ghi đè vùng got của libc để call onegadget hay gì đó
```c
─────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────────
●:22 ► 0x555555555501 <register_hacke>   call   0x5555555552f0              <__isoc99_scanf@p>
        rdi: 0x5555555592b3 ◂— 0x7461685700756c25 /* '%lu' */
        rsi: 0x55555541a0b8 (*ABS*@got.plt) —▸ 0x55555539d400 ◂— endbr64 
        rdx: 0
        rcx: 0x555555314887 (write+23) ◂— cmp rax, -0x1000 /* 'H=' */
      0x555555555506 <register_hacke>   call   0x555555555250              <getchar@plt>
```
