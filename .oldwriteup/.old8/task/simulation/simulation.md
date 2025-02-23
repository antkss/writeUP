# writeup simulation 
- bài sẽ bao gồm các struct để handle command, bài này tạo ra 1 giả lặp thông qua việc nhập các số để dùng được các commands và tính toán giá trị
```c
00000000 struct cmd // sizeof=0x18;variable_size
00000000 {
00000000     unsigned int handler;
00000004     unsigned int cur_cmd;
00000008     unsigned int nb_cmd;
0000000C     unsigned int nextnode;
00000010     char *error_callback;
00000018     struct command command[];
00000018 };

00000000 struct __fixed command // sizeof=0x38
00000000 {                                       // XREF: cmd/r
00000000     size_t func;
00000008     arg arg[3];
00000038 };

00000000 struct __fixed arg // sizeof=0x10
00000000 {                                       // XREF: command/r
00000000     size_t type;
00000008     size_t val;
00000010 };
```
- bài sẽ cho chạy command qua 1 hàm tên là simulate trước rồi mới tới hàm run, khác nhau giữa 2 hàm này đó là hàm simulate sẽ không lưu giá trị tính toán mà chỉ lấy set memsize để có thể malloc ra 1 vùng heap để làm nơi lưu dữ liệu cho hàm run chính là run()
```c
if ( arg->type == 2 )
  {
    if ( arg->val + 8 > mem_size )
      mem_size = arg->val + 8;
    return 0LL;
  }
```
- buffer nhập vào là bao gồm nguyên struct command, và tuân theo các tiêu chuẩn, tuy nhiên xảy ra 1 bug, 1 command bao gồm các biến từ struct cmd trên sẽ được tạo ra từ hàm new_node


```
 type = ptr->command[i].arg[j].type;
 val = ptr->command[i].arg[j].val;
 if ( type > 2 || !check_func(ptr->command[i].func) || type == 1 && val > 4 || type == 2 && val > 0xFFFFFFFE )
            {
              free(ptr);
              puts("Invalid commands");
              return v12 - __readfsqword(0x28u);
            }
```
- khi đọc hàm get_val và store_val có thể thấy nếu type = 1 thì hàm sẽ lưu giá trị hoặc trả về giá trị từ biến re trên bss, type = 2 thì sẽ lưu hoặc trả về trên mem là vùng heap, type 0 thì lưu sẽ trả về giá trị mình nhập tùy thích nhưng sẽ không lưu thông qua type
- có thể thấy rằng index sẽ là val lấy từ struct command mà chúng ta nhập vào tuy nhiên để có thể gây ra oob thì ko thể trực tiếp bằng cách nhập vô vì chương trình đã check kỹ

![image](https://github.com/user-attachments/assets/bc57c117-3ec7-4fac-af6b-361910508d6e)

- hàm run là hàm chạy command, khi chạy sẽ có các chức năng như là +, -, *, / rồi lưu kết quả vào reg hoặc mem, copy giá trị từ reg vào mem,... 
- tuy nhiên khi đọc hàm run có thể thấy
```c
      case 4uLL:
        if ( cur_node->command[cur_node->cur_cmd].arg[0].type == 2 )
          goto LABEL_27;
        errora = resolve_error(cur_node, ip_, 1u);
        if ( !errora )
          goto LABEL_29;
        if ( errora != 1 )
        {
          if ( errora == 2 )
          {
            ip_ = cur_node->handler;
          }
          else
          {
LABEL_27:
            val1 = get_val(&cur_node->command[cur_node->cur_cmd].arg[1]);
            store_val(cur_node->command[cur_node->cur_cmd].arg, val1);
            ++cur_node->cur_cmd;
          }
        }
```
- case 4 hoặc case 5 gì đó sẽ cho phép gán ip_ thông qua handler, quay lại hàm new_node là hàm nhập struct command, có thể thấy điều khiển được giá trị của handler là khả thi, còn nữa, biến handler khi nhập vào không check bound
- chính vì vậy khi chạy lần lặp thứ 2 của while trong hàm run, node sẽ được run từ index là _ip chương trình bị oob
```c
  checkcircle = 0;
  while ( checkcircle <= 0x5000 )
  {
    cur_node = node_list[ip_];
```asm
pwndbg> tel 0x555555559080
00:0000│  0x555555559080 (node_list) ◂— 0
01:0008│  0x555555559088 (node_list+8) —▸ 0x55555555d2a0 ◂— 0
02:0010│  0x555555559090 (node_list+16) —▸ 0x55555555d300 ◂— 0
03:0018│  0x555555559098 (node_list+24) —▸ 0x55555555d360 ◂— 0
04:0020│  0x5555555590a0 (node_list+32) —▸ 0x55555555d3c0 ◂— 0
05:0028│  0x5555555590a8 (node_list+40) —▸ 0x55555555d420 ◂— 0
...
fe:07f0│  0x555555559870 (node_list+2032) ◂— 0
ff:07f8│  0x555555559878 (node_list+2040) ◂— 0
pwndbg> 
100:0800│  0x555555559880 (ip) ◂— 1
101:0808│  0x555555559888 ◂— 0
102:0810│  0x555555559890 ◂— 0
103:0818│  0x555555559898 ◂— 0
104:0820│  0x5555555598a0 (re) ◂— 0
105:0828│  0x5555555598a8 (re+8) ◂— 0
106:0830│  0x5555555598b0 (re+16) ◂— 0
107:0838│  0x5555555598b8 (re+24) ◂— 0
pwndbg> 
108:0840│  0x5555555598c0 (re+32) ◂— 0
109:0848│  0x5555555598c8 (mem) —▸ 0x55555555d780 ◂— 0
```
- mà mem thì nằm dưới node_list do đó có thể hoàn toàn run đc node là địa chỉ từ mem nếu như có đủ thành phần của 1 struct cmd
- mà mem thì có thể tự do truy cập gán giá trị nên có thể fake 1 node sao cho nó có thể tính toán, tận dụng chức năng của chương trình để có thể lấy được địa chỉ system, vì trong struct cmd có 1 element là error_callback
```c
    }
    else if ( ((unsigned int (__fastcall *)(cmd *, _QWORD, _QWORD))cur_node->error_callback)(cur_node, ip, num) )
    {
      return 0LL;
```
- sẽ được gọi thông qua 1 hàm ở command 4 hoặc 5
- vì thế có thể thay thế error_callback thành system và sau đó run node với command là 4 hoặc 5
- để có được điều đó thì cần phải tạo ra 1 số âm ở element tên val của fake struct cmd trong mem
- sau đó có thể gọi node từ mem để có thể dùng được
```
unsigned __int64 __fastcall get_val(arg *arg)
...
    if ( result )
    {
      if ( result == 1 )
        return re[arg->val];
    }
    else
    {
```
- khi đó có thể lấy được giá trị từ bss có thể là địa chỉ libc sau đó thực hiện phép toán với 1 hằng số để tạo ra địa chỉ system sau đó tiếp theo là gán địa chỉ đó vào 1 node nào đó với command là 4 hoặc 5
- có thể thấy khi gọi hàm ở error_callback thì tham số vào là địa chỉ phần tử đầu của struct nên có thể gán phần tử đầu của struct với giá trị là sh là có thể lấy shell
