from pwn import p32,p64,p16,p8
class _IO_FILE():
   def __init__(self):
       self._flags=0;
       self.hole1=0;
       self._IO_read_ptr=0;
       self._IO_read_end=0;
       self._IO_read_base=0;
       self._IO_write_base=0;
       self._IO_write_ptr=0;
       self._IO_write_end=0;
       self._IO_buf_base=0;
       self._IO_buf_end=0;
       self._IO_save_base=0;
       self._IO_backup_base=0;
       self._IO_save_end=0;
       self._markers=0;
       self._chain=0;
       self._fileno=0;
       self._flags2=0;
       self._old_offset=0xffffffffffffffff;
       self._cur_column=0;
       self._vtable_offset=0;
       self._shortbuf=0;
       self.hole2=0;
       self._lock=0;
       self._offset=0xffffffffffffffff;
       self._codecvt=0;
       self._wide_data=0;
       self._freeres_list=0;
       self._freeres_buf=0;
       self._pad5=0;
       self._mode=0;
       self._unused2 = 0;
       self.vtable = 0
   def create(self):
       payload = b""
       payload += p32(self._flags);
       payload += p32(self.hole1)
       payload += p64(self._IO_read_ptr);
       payload += p64(self._IO_read_end);
       payload += p64(self._IO_read_base);
       payload += p64(self._IO_write_base);
       payload += p64(self._IO_write_ptr);
       payload += p64(self._IO_write_end);
       payload += p64(self._IO_buf_base);
       payload += p64(self._IO_buf_end);
       payload += p64(self._IO_save_base);
       payload += p64(self._IO_backup_base);
       payload += p64(self._IO_save_end);
       payload += p64(self._markers);
       payload += p64(self._chain);
       payload += p32(self._fileno);
       payload += p32(self._flags2);
       payload += p64(self._old_offset);
       payload += p16(self._cur_column);
       payload += p8(self._vtable_offset);
       payload += p8(self._shortbuf);
       payload += p32(self.hole2)
       payload += p64(self._lock);
       payload += p64(self._offset);
       payload += p64(self._codecvt);
       payload += p64(self._wide_data);
       payload += p64(self._freeres_list);
       payload += p64(self._freeres_buf);
       payload += p64(self._pad5);
       payload += p32(self._mode);
       payload += self._unused2.to_bytes(20, byteorder='big');
       payload += p64(self.vtable)
       return payload
   def structure(self):
       print(f"""
            /* offset      |    size */  type = struct _IO_FILE {{
            /*      0      |       4 */    int _flags = {hex(self._flags)};
            /* XXX  4-byte hole      */
            /*      8      |       8 */    char *_IO_read_ptr= {hex(self._IO_read_ptr)};
            /*     16      |       8 */    char *_IO_read_end= {hex(self._IO_read_end)};
            /*     24      |       8 */    char *_IO_read_base= {hex(self._IO_read_base)};
            /*     32      |       8 */    char *_IO_write_base= {hex(self._IO_write_base)};
            /*     40      |       8 */    char *_IO_write_ptr= {hex(self._IO_write_ptr)};
            /*     48      |       8 */    char *_IO_write_end= {hex(self._IO_write_end)};
            /*     56      |       8 */    char *_IO_buf_base= {hex(self._IO_buf_base)};
            /*     64      |       8 */    char *_IO_buf_end= {hex(self._IO_buf_end)};
            /*     72      |       8 */    char *_IO_save_base= {hex(self._IO_save_base)};
            /*     80      |       8 */    char *_IO_backup_base= {hex(self._IO_backup_base)};
            /*     88      |       8 */    char *_IO_save_end= {hex(self._IO_save_end)};
            /*     96      |       8 */    struct _IO_marker *_markers= {hex(self._markers)};
            /*    104      |       8 */    struct _IO_FILE *_chain= {hex(self._chain)};
            /*    112      |       4 */    int _fileno= {hex(self._fileno)};
            /*    116      |       4 */    int _flags2= {hex(self._flags2)};
            /*    120      |       8 */    __off_t _old_offset= {hex(self._old_offset)};
            /*    128      |       2 */    unsigned short _cur_column= {hex(self._cur_column)};
            /*    130      |       1 */    signed char _vtable_offset= {hex(self._vtable_offset)};
            /*    131      |       1 */    char _shortbuf[1] = {hex(self._shortbuf)};
            /* XXX  4-byte hole      */
            /*    136      |       8 */    _IO_lock_t *_lock = {hex(self._lock)};
            /*    144      |       8 */    __off64_t _offset = {hex(self._offset)};
            /*    152      |       8 */    struct _IO_codecvt *_codecvt = {hex(self._codecvt)};
            /*    160      |       8 */    struct _IO_wide_data *_wide_data = {hex(self._wide_data)};
            /*    168      |       8 */    struct _IO_FILE *_freeres_list = {hex(self._freeres_list)};
            /*    176      |       8 */    void *_freeres_buf = {hex(self._freeres_buf)};
            /*    184      |       8 */    size_t __pad5 = {hex(self._pad5)};
            /*    192      |       4 */    int _mode = {hex(self._mode)};
            /*    196      |      20 */    char _unused2[20] = {hex(self._unused2)};

                                           /* total size (bytes):  216 */
                                           vtable: {hex(self.vtable)}
                                           payload size: {len(self.create())}
                                         }}
             """)

