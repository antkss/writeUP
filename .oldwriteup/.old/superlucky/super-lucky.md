# write up superlucky 
- vì bài có out of bound nên có thể nhập số âm để leak libc 
- sau khi có libc thì tính được offset để tính index đến các nơi khác để leak, từ đó có thể leak được state, vùng này được tạo ra để chứa các giá trị random 
- phải leak vì bài đã xóa mất seed sau khi tạo seed vào srand từ urandom
```c
      int32_t *fptr = buf->fptr;
      int32_t *rptr = buf->rptr;
      int32_t *end_ptr = buf->end_ptr;
      uint32_t val;

      val = *fptr += (uint32_t) *rptr;
      /* Chucking least random bit.  */
      *result = val >> 1;
      ++fptr;
      if (fptr >= end_ptr)
	{
	  fptr = state;
	  ++rptr;
	}
      else
	{
	  ++rptr;
	  if (rptr >= end_ptr)
	    rptr = state;
	}
      buf->fptr = fptr;
      buf->rptr = rptr;
    }
  return 0;
```
- bài sẽ dùng fptr và rptr để track 2 địa chỉ chứa 2 giá trị trong state sau đó cộng 2 giá trị đó rồi dịch phải 1 bit rồi tăng idx lên để tiếp tục cộng 2 giá trị khác và gán lại cho 1 trong 2 ptr nếu như địa chỉ trong ptr đó > end_ptr trong struct và cuối cùng là gán lại cho fptr và rptr trong struct
- cách làm là sẽ leak hết số lần có thể leak từ state và bắt đầu từ rptr và fptr đầu tiên thông qua debug gdb, sau đó làm theo công thức để tính ra số random rồi lưu nó lại list, các lần tiếp theo cứ tính theo công thức kết hợp với giá trị state đã tính từ list để tính số random, cuối cùng là gửi vào chương trình là lấy được flag
```bash
    [*] Process '/home/as/pwnable/writeup/superlucky/super-luckye' stopped with exit code 0 (pid 13629)
    [DEBUG] Received 0x24 bytes:
        b'flag{fdskahfdskajfhdsakfdashfjkds}\n'
        b'\n'
    flag{fdskahfdskajfhdsakfdashfjkds}

    [*] Got EOF while reading in interactive
    $  

```

