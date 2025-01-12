# pwn_ll
- khi tạo 1 chunk, chương trình sẽ đi hết từ chunk đầu đã được định nghĩa sẵn đến chunk cuối cùng và add chunk mới tạo vào link list 

```c
        for ( ptr = random; ptr; ptr = ptr->next )
          last = ptr;
        last->next = array;
```
- khi xóa chunk thì con trỏ sẽ được xóa nên không có uaf ở biến chunk 
```c
        printf("Index: ");
        scanf("%u", &idx);
        getchar();
        if ( idx > 4 || !chunk[idx] )
        {
          puts("Invalid index");
          exit(-1);
        }
        free(chunk[idx]);
        chunk[idx] = 0LL;
        puts("Remove name successfully");
```
- tuy nhiên khi 1 heap chunk được free chỉ có 0x10 bytes đầu bị thay đổi, còn lại vẫn được giữ nguyên
- vì vậy next pointer trong trường hợp này vẫn được dữ nguyên trong malloc chunk 
struct của 1 chunk như sau: 
```
00000000 struct lmao // sizeof=0x210
00000000 {
00000000     number *number;
00000008     char lmao8[504];
00000200     int id;
00000204     int nByte;
00000208     lmao *next;
00000210 };
```
- vì vậy khi tạo 1 chunk mới thì malloc sẽ lấy lại chunk cũ đã được free sau đó traverse đến pointer cuối cùng, vì lúc này pointer cuối vẫn giữ nguyên nên từ đó có thể control sao cho có 1 địa chỉ next nằm trên 2 chunk khác nhau, khi free chunk còn lại thì có thể leak được địa chỉ heap
- tuy nhiên sau khi leak địa chỉ thì sẽ hình thành 1 vòng tròn khép kín của các chunk vì vậy không allocate chunk mới được, tuy nhiên có thêm option 5 để allocate lần nữa 1 chunk trong link list đã bị free sau đó overwrite làm mất next pointer để có thể làm các bước control tiếp theo 
- bằng việc kết hợp với options 5 có thể control được cả nByte là số byte ghi của chương trình vào 1 chunk, vì thế có thể ghi lan sang chunk tiếp theo và sau đó có thể sử dụng chunk đã free để malloc sang 1 exotic chunk nào đó như là rip của hàm main

