# writeup sandbox utctf
- bài cho 2 file 1 là file binary với lỗi buffer overflow cơ bản và thứ 2 là 1 file tên loader được dùng làm sandbox để run file binary
- decompile file sandbox
```c
      push_stack(v11, *v6);
    }
    push_stack(v11, v16);
    uc_reg_read(v11, 44LL, &v12);
    uc_reg_write(v11, 36LL, &v12);
    uc_hook_add(v11, (unsigned int)&v13, 48, (unsigned int)hook_mem_invalid, 0, 1, 0LL);
    uc_hook_add(v11, (unsigned int)&v14, 2, (unsigned int)hook_syscall, 0, 1, 0LL);
    uc_emu_start(v11, v10, -1LL, 0LL, 0LL);
    uc_close(v11);
    v3 = 0;
```
- về cơ bản thì chương trình spam 1 đống hàm có tên khá là quy cách: uc_reg_read, uc_reg_write, ... mấy hàm này là hàm được gọi từ 1 thư viện khác và ko phải được code, prefix giống nhau, tra google thì thấy nó của 1 engine chuyên dùng giả lập: unicorn
- đọc docs có thể biết được chức năng của từng hàm
```c
  file_name = argv[1];
  std::map<std::string,section>::map(v18, argv, envp);
  std::map<int,segment>::map(v19);
  v9 = parse_elf(file_name, &v10, v18, v19);
...
 if ( (unsigned int)uc_open(4LL, 8LL, &v11) )
  {
...
    push_stack(v11, v16);
    uc_reg_read(v11, 44LL, &v12);
    uc_reg_write(v11, 36LL, &v12);
    uc_hook_add(v11, (unsigned int)&v13, 48, (unsigned int)hook_mem_invalid, 0, 1, 0LL);
    uc_hook_add(v11, (unsigned int)&v14, 2, (unsigned int)hook_syscall, 0, 1, 0LL);
    uc_emu_start(v11, v10, -1LL, 0LL, 0LL);
    uc_close(v11);
```
- file được đọc từ arg[1] sau đó được run
- thấy rằng có 1 hàm đó là hook_syscall, chính xác thì bug nằm trong đây, hook_syscall là hàm được add vào hook khi chạy giả lập để handle syscall cho chương trình giả lập
```c
 uc_reg_read(a1, 35, (__int64)&sysno);
  uc_reg_read(a1, 39, (__int64)fd);
  uc_reg_read(a1, 43, (__int64)&v20);
  uc_reg_read(a1, 40, (__int64)&nbytes)
...
  else if ( sysno )
  {
    switch ( sysno )
    {
      case 1LL:
        uc_mem_read(v14, v20, s, nbytes);
        printf("\x1B[33m>>> syscall write\x1B[0m(fd=%d, *buf='%s', count=%d)\n", fd[0], s, nbytes);
        uc_reg_write(v14, 35LL, &nbytes);
        break;
      case 20LL:
...
```
- syscall sẽ được đọc vào sysno và sau đó thông qua switch case để tìm syscall phù hợp 
- quay lại với file binary bị buffer overflow thì binary sẽ có đủ các gadgets cần thiết để thực hiện syscall
- khi thực hiện syscall sẽ thông qua hook_syscall để xử lý
- với hàm uc_reg_read sẽ có 3 tham số:
```bash
uc_reg_read

NOTE: If UC_MODE is 32-bit and regid is 64-bit register, value is 0 and uc_reg_read returns NO error (UC_ERROK).

uc_err uc_reg_read(uc_engine *uc, int regid, void *value)
```
- tham số đầu là struct của engine được tạo ra trong quá trình chạy binary, tham số thứ 2 là id thanh ghi giả lặp được đọc giá trị vào, tham số thứ 3 là giá trị
- thư ở trên giá trị được đọc theo id thì sẽ là rax, rdi, rsi, rdx
- bài sẽ có 2 bug:
- thứ 1: buffer overflow sandbox
```c
   *(size_t *)((char *)&v9 + (v2 & 0xFFF) - 8) = *(size_t *)((char *)&v9 + (v2 & 0xFFF) - 8);
    buf = &v9;
    v22 = read(rdi[0], &v9, rdx);
    uc_reg_write(v14, 35LL, &v22);
    uc_mem_write(v14, rsi, buf, rdx, v4, v5, v9, v10, v11, v12, v13);
```

- rdx là giá trị mà có thể điều khiển thông qua chương trình chạy trên sandbox, do đó khi rdx quá lớn dẫn tới buffer vì v9 vốn bị giới hạn
- tuy nhiên bug này ko dùng đc, bug thứ 2 là integer overflow
```
 if ( sysno == 1024 )
  {
    v31 = *(_QWORD *)rdi - 8323072LL;
    *(_DWORD *)((char *)&stack + *(_QWORD *)rdi - 8323072) = syscall_cnt;
  }
```
- với rax = 1024 thì có thể gọi syscall này, syscall sẽ gán giá trị của syscall_cnt vào stack[index] index là phép tính bao gồm rdi có thể control nên dễ dàng sửa đổi được dữ liệu từ vùng bss do biến stack nằm trên vùng bss
- syscall_cnt là biến tăng sau mỗi lần chạy 1 syscall
- quan sát ở dưới thì thấy có phần default của switch case chính là lúc gọi các syscall khác các syscall trên
  ```
       default:
        v15 = 0;
        for ( j = 0; (unsigned __int64)j <= 1; ++j )
        {
          if ( exit_syscalls[j] == sysno )
            syscall(sysno, *(_QWORD *)rdi, rsi, rdx);
        }
        printf(">>> enumation stoped because of invalid syscall %d\n", sysno);
  ```
  - khi gọi syscall không hợp lệ thì chương trình sẽ so sánh nếu syscall là 1 trong các syscall được cho phép dùng để exit chương trình hay không, nếu không thì chương trình báo lỗi, tuy nhiên array chứa các syscall exit là ext_syscalls nằm ở vùng bss, do đó có thể thay thế thông qua syscall 1024
- idea là thay đổi 1 trong 2 giá trị của mảng thành 0x3b và có thể thực thi shellcode
- còn về phần syscall_cnt có thể control thông qua việc gọi 0x3b lần syscall hợp lệ để có được giá trị ghi vào exit_syscalls
