# write up bflat
```c
  puts("Input sort type (1 = forward, 2 = reverse):");
  __isoc99_scanf("%d");
  qsort(base, v4, 4uLL, (__compar_fn_t)*(&cmps + v5 - 1));
```
- chương trình có sử dụng qsort để sort các phần tử, chương trình đã lưu sẵn 2 hàm sort ở .bss và dùng index để truy cập chọn hàm 
- tuy nhiên index kiểu int nhưng không check dẫn đến bị oob và có thể thực thi bất kỳ thứ gì ở bss
- ta có thể trỏ tới got để thực thi printf từ đó có thể dùng format string 
- vì format string chỉ có thể dùng ghi 1 lần nên phải làm payload sao cho trong 1 lần ghi, hàm system được thực thi 

