## khái niệm vtable 
https://en.wikipedia.org/wiki/Virtual_method_table
## _IO_FILE
```c 
struct _IO_FILE_plus
{
  FILE file;
  const struct _IO_jump_t *vtable;
};
```
- trong chương trình thông thường sẽ bắt gặp 3 con trỏ trỏ tới 3 địa chỉ thuộc vùng ghi được của libc, các stream này có nhiệm vụ điều phối input, output của chương trình
```assembly
00:0000│  0x404020 (stdout@GLIBC_2.2.5) —▸ 0x7ffff7f915c0 (_IO_2_1_stdout_) ◂— 0xfbad2887
01:0008│  0x404028 ◂— 0
02:0010│  0x404030 (stdin@GLIBC_2.2.5) —▸ 0x7ffff7f908e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
03:0018│  0x404038 ◂— 0
04:0020│  0x404040 (stderr@GLIBC_2.2.5) —▸ 0x7ffff7f914e0 (_IO_2_1_stderr_) ◂— 0xfbad2087```
```
- tuy nhiên 3 con trỏ này thuộc vùng ghi được của binary, nên bằng 1 cách nào đó, có thể là malloc, có thể là gì đó thì sẽ bị ghi đè 1 cách dễ dàng-  vì 3 địa chỉ libc trên trỏ tới struct có kiểu dữ liệu _IO_FILE_plus nên ta có thể fake struct này để nó thực  hiện những gì mà mình mong muốn 
```c


            /* offset      |    size */  type = struct _IO_FILE {
            /*      0      |       4 */    int _flags = 0x733b0810;
            /* XXX  4-byte hole      */
            /*      8      |       8 */    char *_IO_read_ptr= 0x0;
            /*     16      |       8 */    char *_IO_read_end= 0x0;
            /*     24      |       8 */    char *_IO_read_base= 0x0;
            /*     32      |       8 */    char *_IO_write_base= 0x0;
            /*     40      |       8 */    char *_IO_write_ptr= 0x0;
            /*     48      |       8 */    char *_IO_write_end= 0x0;
            /*     56      |       8 */    char *_IO_buf_base= 0x0;
            /*     64      |       8 */    char *_IO_buf_end= 0x0;
            /*     72      |       8 */    char *_IO_save_base= 0x0;
            /*     80      |       8 */    char *_IO_backup_base= 0x0;
            /*     88      |       8 */    char *_IO_save_end= 0x0;
            /*     96      |       8 */    struct _IO_marker *_markers= 0x0;
            /*    104      |       8 */    struct _IO_FILE *_chain= 0x0;
            /*    112      |       4 */    int _fileno= 0x0;
            /*    116      |       4 */    int _flags2= 0x0;
            /*    120      |       8 */    __off_t _old_offset= 0xffffffffffffffff;
            /*    128      |       2 */    unsigned short _cur_column= 0x0;
            /*    130      |       1 */    signed char _vtable_offset= 0x0;
            /*    131      |       1 */    char _shortbuf[1] = 0x0;
            /* XXX  4-byte hole      */
            /*    136      |       8 */    _IO_lock_t *_lock = 0x75a8b1847710;
            /*    144      |       8 */    __off64_t _offset = 0xffffffffffffffff;
            /*    152      |       8 */    struct _IO_codecvt *_codecvt = 0x0;
            /*    160      |       8 */    struct _IO_wide_data *_wide_data = 0x4041f0;
            /*    168      |       8 */    struct _IO_FILE *_freeres_list = 0x0;
            /*    176      |       8 */    void *_freeres_buf = 0x0;
            /*    184      |       8 */    size_t __pad5 = 0x0;
            /*    192      |       4 */    int _mode = 0x0;
            /*    196      |      20 */    char _unused2[20] = 0x6161616161616161616161616161616161616161;

                                           /* total size (bytes):  216 */
                                           vtable: 0x75a8b18443a8
                                           payload size: 224
                                         }
             
```
- về cơ bản thì đây sẽ là toàn bộ struct của _IO_FILE_plus
- cái mình quan tâm sẽ là cái vtable,có thể nhận ra rằng ta có thể fake luôn cả vtable, nhưng mà nó check hết cả r =)))
```
  if (__glibc_unlikely (offset >= section_length))
    /* The vtable pointer is not in the expected section.  Use the
       slow path, which will terminate the process if necessary.  */
    _IO_vtable_check ();
  return vtable;
}
```
- cách check thì cũng khá đơn giản để hiểu, nếu vtable mà bị dính fake, thì nó nhảy sang check kỹ hơn 
```c
void attribute_hidden
_IO_vtable_check (void)
{
#ifdef SHARED
  /* Honor the compatibility flag.  */
  void (*flag) (void) = atomic_load_relaxed (&IO_accept_foreign_vtables);
  PTR_DEMANGLE (flag);
  if (flag == &_IO_vtable_check)
    return;

  /* In case this libc copy is in a non-default namespace, we always
     need to accept foreign vtables because there is always a
     possibility that FILE * objects are passed across the linking
     boundary.  */
  {
    Dl_info di;
    struct link_map *l;
    if (!rtld_active ()
        || (_dl_addr (_IO_vtable_check, &di, &l, NULL) != 0
            && l->l_ns != LM_ID_BASE))
      return;
  }

#else /* !SHARED */
  /* We cannot perform vtable validation in the static dlopen case
     because FILE * handles might be passed back and forth across the
     boundary.  Therefore, we disable checking in this case.  */
  if (__dlopen != NULL)
    return;
#endif

  __libc_fatal ("Fatal error: glibc detected an invalid stdio handle\n");
}
```
-lần này nó check con trỏ, ở đoạn này nếu như có cơ hội ghi vào vùng fs:0x30 thì có khả năng sẽ bypass
```assembly
### _IO_vtable_check function
   0x00007ffff7e5e6b0 <+0>:	lea    rdi,[rip+0xfffffffffffffff9]        # 0x7ffff7e5e6b0 <_IO_vtable_check>
   0x00007ffff7e5e6b7 <+7>:	mov    rax,QWORD PTR [rip+0x1561ea]        # 0x7ffff7fb48a8 <IO_accept_foreign_vtables>
   0x00007ffff7e5e6be <+14>:	ror    rax,0x11
   0x00007ffff7e5e6c2 <+18>:	xor    rax,QWORD PTR fs:0x30
=> 0x00007ffff7e5e6cb <+27>:	cmp    rax,rdi
```
- đây được gọi là 1 vtable trong số nhiều vtables khác nhau 
```c
  /* _IO_file_jumps  */
  [IO_FILE_JUMPS] = {
    JUMP_INIT_DUMMY,
    JUMP_INIT (finish, _IO_file_finish),
    JUMP_INIT (overflow, _IO_file_overflow),
    JUMP_INIT (underflow, _IO_file_underflow),
    JUMP_INIT (uflow, _IO_default_uflow),
    JUMP_INIT (pbackfail, _IO_default_pbackfail),
    JUMP_INIT (xsputn, _IO_file_xsputn),
    JUMP_INIT (xsgetn, _IO_file_xsgetn),
    JUMP_INIT (seekoff, _IO_new_file_seekoff),
    JUMP_INIT (seekpos, _IO_default_seekpos),
    JUMP_INIT (setbuf, _IO_new_file_setbuf),
    JUMP_INIT (sync, _IO_new_file_sync),
    JUMP_INIT (doallocate, _IO_file_doallocate),
    JUMP_INIT (read, _IO_file_read),
    JUMP_INIT (write, _IO_new_file_write),
    JUMP_INIT (seek, _IO_file_seek),
    JUMP_INIT (close, _IO_file_close),
    JUMP_INIT (stat, _IO_file_stat),
    JUMP_INIT (showmanyc, _IO_default_showmanyc),
    JUMP_INIT (imbue, _IO_default_imbue)
  },

-> vtables.c glibc 2.39
```
- các địa chỉ của các hàm mà nó có thể jmp đều ở trong đây, tuy nhiên vì vtable không thể check địa chỉ nào mà mình không được jmp nên mình có thể làm lệch địa chỉ vtable trong _IO_FILE_plus để nó jmp vào hàm mình cần 
- ta jmp vào các hàm này vì có thể nó có chứa các lệnh call hoặc jmp mà ta có thể điều khiển được tham số 
```assembly
00:0000│  0x7ffff7fb1250 (_IO_file_jumps) ◂— 0
01:0008│  0x7ffff7fb1258 (_IO_file_jumps+8) ◂— 0
02:0010│  0x7ffff7fb1260 (_IO_file_jumps+16) —▸ 0x7ffff7e5f280 (__GI__IO_file_finish) ◂— push rbp
03:0018│  0x7ffff7fb1268 (_IO_file_jumps+24) —▸ 0x7ffff7e5fda0 (__GI__IO_file_overflow) ◂— push r12
04:0020│  0x7ffff7fb1270 (_IO_file_jumps+32) —▸ 0x7ffff7e5f990 (__GI__IO_file_underflow) ◂— mov eax, dword ptr [rdi]
05:0028│  0x7ffff7fb1278 (_IO_file_jumps+40) —▸ 0x7ffff7e61d20 (_IO_default_uflow) ◂— push rbp
06:0030│  0x7ffff7fb1280 (_IO_file_jumps+48) —▸ 0x7ffff7e62fa0 (_IO_default_pbackfail) ◂— push r15
07:0038│  0x7ffff7fb1288 (_IO_file_jumps+56) —▸ 0x7ffff7e608a0 (__GI__IO_file_xsputn) ◂— xor eax, eax
pwndbg> 
08:0040│  0x7ffff7fb1290 (_IO_file_jumps+64) —▸ 0x7ffff7e60a90 (__GI__IO_file_xsgetn) ◂— push r15
09:0048│  0x7ffff7fb1298 (_IO_file_jumps+72) —▸ 0x7ffff7e600e0 (__GI__IO_file_seekoff) ◂— push r15
0a:0050│  0x7ffff7fb12a0 (_IO_file_jumps+80) —▸ 0x7ffff7e620a0 (_IO_default_seekpos) ◂— push rbx
0b:0058│  0x7ffff7fb12a8 (_IO_file_jumps+88) —▸ 0x7ffff7e5f8d0 (__GI__IO_file_setbuf) ◂— push rbx
0c:0060│  0x7ffff7fb12b0 (_IO_file_jumps+96) —▸ 0x7ffff7e5ffa0 (__GI__IO_file_sync) ◂— push rbp
0d:0068│  0x7ffff7fb12b8 (_IO_file_jumps+104) —▸ 0x7ffff7e539b0 (_IO_file_doallocate) ◂— push r12
0e:0070│  0x7ffff7fb12c0 (_IO_file_jumps+112) —▸ 0x7ffff7e60790 (_IO_file_read) ◂— test byte ptr [rdi + 74h], 2
....
```
- giả sử 1 vtable tính từ địa chỉ này đi xuống, và ta muốn hàm fwrite sẽ jmp, nhưng mặc định fwrite jmp vào 
```assembly
07:0038│  0x7ffff7fb1288 (_IO_file_jumps+56) —▸ 0x7ffff7e608a0 (__GI__IO_file_xsputn) ◂— xor eax, eax
```
- vì thế nên để nó jmp vào 1 hàm khác như __GI__IO_file_overflow
thì con địa chỉ của vtable chứa trong _IO_FILE_plus fake phải trừ đi offset sẽ là 0x20
- ví dụ về bài bytecode này là 1 ví dụ về 1 path, ngoài ra còn rất nhiều path có thể ta chưa khám phá được, may be có thể sử dụng angr để tự động tìm khá ok


