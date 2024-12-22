# database
- chương trình tồn tại 3 bug
- chương trình sử dụng memory pool để quản lý bộ nhớ và sử dụng queue để thêm và lấy dữ liệu như 1 database
- đầu tiên đó là overflow ở heap nhưng bug này không để làm gì vì chỉ overflow được đến size của chunk tiếp theo
- memory pool trong chương trình được chia thành các kích thước như này
```len2            dd 10h, 20h, 40h, 80h, 100h, 200h, 400h, 800h, 1000h, 3 dup(0)```
- kích thước khi allocate chỉ cho phép nhỏ hơn 0x1000
- các ô nhớ được mmap sẵn và lưu trong 1 array global
- ngoài ra chương trình allocate thêm các chunk malloc tương ứng và lưu vào 1 array có kích thước tương tự để đánh dấu chunk đã được free hay không
- khi sử dụng memory pool, chương trình cho phép tạo 1 vùng nhớ với kích thước cố định tuy nhiên do không xóa bộ nhớ khi free nên khi allocate lại thì dữ liệu vẫn còn, chương trình giới hạn kích thước 1 chunk nhớ chỉ có 0xff0 nên khi quá kích thước chương trình sẽ tự động tạo thêm 1 ô nhớ nữa và tìm kiếm kích thước phù hợp
-  giả sử kích thước khi tạo là 0xff0 + 0x8
- khi allocate lần đầu: chunk được tạo với kích thước nhỏ hơn 0x1000
```chunk_ = (char *)allocate(size2_ + 16);```
- khi còn dư size thì sẽ được allocate lần 2 và với kích thước 0x8 lần này chunk 0x10 thỏa mãn bằng 0x10
```  chunk = (char *)allocate(size + 8);```
- tuy nhiên khi xóa chunk thì chương trình sẽ không xóa dữ liệu mà chỉ set bit cho các chunk malloc nên dữ liệu vẫn còn
- struct của chunk đầu sẽ có thêm phần size còn chunk thứ 2 thì không có nên chunk 2 coi như ghi lệnh 8 bytes đi lên đồng nghĩa với việc khi allocate lần 2 với size 0x8 thì xảy ra trường hợp next pointer có thể bị control, tuy nhiên bug này không cần đến lắm
- tiếp theo đó là việc overflow
```c
unsigned int __fastcall func_data(queue *data, queue *src)
{
  unsigned int data_size_; // ecx
  unsigned int size_copy2; // ecx
  unsigned int data_size; // [rsp+14h] [rbp-2Ch]
  unsigned int size_copy1; // [rsp+14h] [rbp-2Ch]
  unsigned int final_size; // [rsp+14h] [rbp-2Ch]
  unsigned int size; // [rsp+14h] [rbp-2Ch]

  data_size = data->size;
  if ( src[1].size + src->size > 0xFFE - data->size )
    return -1879048192;
  if ( memchr(src->value, ',', src->size) || memchr(src[1].value, ',', src[1].size) )
    return -1879048188;
  data_size_ = data_size;
  size_copy1 = data_size + 1;
  data->value[data_size_] = 0x2C;
  memcpy(&data->value[size_copy1], src->value, src->size);
  size_copy2 = size_copy1 + src->size;
  final_size = size_copy2 + 1;
  data->value[size_copy2] = 0x3D;
  memcpy(&data->value[size_copy2 + 1], src[1].value, src[1].size);
  size = final_size + src[1].size;
  data->value[size] = 0;
  data->size = size;
  return 0;
}
```
- chương trình cho phép gọi hàm này thông qua option 4 để copy dữ liệu người dùng nhập vào phần data của 1 struct function khi đã push vào queue
- 1 struct function kiểu: 
```c
00000000 struct fun_queues // sizeof=0x10
00000000 {
00000000     func *fun;
00000008     func_data *data;
00000010 };
00000000 struct __fixed func_data // sizeof=0x8
00000000 {
00000000     queue *queue;
00000008 };
```
- tuy nhiên dữ liệu có thể copy vào đó nhiều lần nên xảy ra overflow vùng nhớ mmap, vì thế khi tạo 1 chunk khác mà size > 0xff0 nằm ở dưới chunk data của func_queue thì có thể control được forward pointer hoặc là size của chunk đó, khi đó chương trình có option 3 dùng để dequeue và in ra phần dữ liệu có trong queue dưới dạng hex, vì vậy có thể leak được nhiều địa chỉ bên dưới 1 chunk
- idea là tạo ra 1 chunk size 0x1000 tương ứng nằm dưới có forward là chunk đầu của pool tương ứng với kích thước 0x10 và tạo ra func_queue có chunk data là chunk đầu của 0x1000 và chunk của func sẽ là chunk 0x10 tiếp theo, sau đó overwrite size của chunk 0x1000 ở dưới lớn hơn ban đầu và sau đó sẽ leak được địa chỉ exe chứa trong chunk của func
- tiếp theo leak libc bằng cách dùng địa chỉ exe bằng phương pháp tương tự, rồi tiếp theo có thể overwrite nhiều lần để đến được tới func_queue để có thể overwrite phần chứa địa chỉ hàm call
```assembly
02:0010│  0x55555554e010 —▸ 0x555555559028 —▸ 0x5555555557c0 ◂— push rbp
03:0018│  0x55555554e018 —▸ 0x55555554e020 ◂— 0x24fed
04:0020│  0x55555554e020 ◂— 0x24fed
05:0028│  0x55555554e028 —▸ 0x555555529000 ◂— 0x616161616161612c (',aaaaaaa')
06:0030│  0x55555554e030 ◂— 0
07:0038│  0x55555554e038 ◂— 0
```
- thành system
```assembly
02:0010│  0x55555554e010 —▸ 0x55555554cfef —▸ 0x555555258740 (system) ◂— endbr64 
03:0018│  0x55555554e018 —▸ 0x5555553cb42f ◂— 0x68732f6e69622f /* '/bin/sh' */
04:0020│  0x55555554e020 ◂— 0x55550002503e
05:0028│  0x55555554e028 —▸ 0x555555529000 ◂— 0x616161616161612c (',aaaaaaa')
06:0030│  0x55555554e030 ◂— 0x3d /* '=' */
```
- và khi gọi thì hàm system sẽ được call 
