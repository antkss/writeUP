# write up chat
- mô tả: bài chat sẽ cung cấp cho ta port để kết nối mặc định là 10000, khi kết nối ta có thể gửi buffer để control được chương trình, buffer được đưa vào parse ra và sau đó gán giá trị cho các phần của 1 struct
- tất cả các connection đều được nhận bằng cùng 1 biến là s 
```
  while ( 1 )
  {
    return_value = accept(fd, &addr, &addr_len);
    while ( s )
      ;
    v3 = ntohs(*(uint16_t *)addr.sa_data);
    v4 = inet_ntoa(*(struct in_addr *)&addr.sa_data[2]);
    printf("New connection to recv sock from %s:%d\n", v4, v3);
    s = return_value;
    pthread_create(&newthread, 0LL, (void *(*)(void *))client_handler, &s);
  }
```
- biến s sau khi truyền vào hàm client_handler thì sẽ nhận data và đưa vào handle_recv để sử lý
```
  if ( (unsigned int)recv(data->received_of_receive, &buf, 4uLL, 0) )
  {
    if ( !buf )
      handle_recv(data);
```
- vì cùng dùng chung biến s nên khi có 2 client kết nối song song thì sẽ xảy ra race condition
#### exploit 
- có 4 lần recv trong client-handler,2 lần nhận đầu tiên dùng để nhận size cho 2 lần dưới,  khi lần 2 kết thúc thì sẽ nhận size của lần thứ 4:
```
  receivedd = recv(fd, buf, (unsigned int)receive_data->msg, 0);
```
- khi lần recv thứ 3 kết thúc thì lúc này chờ cho lần nhập thứ 4, nhưng giả sử nếu ta kết nối 1 client nữa vào server và cho size lớn hơn, thì lúc đó biến chứa size sẽ thay đổi vì server dùng 1 biến nhận data duy nhất, khi quay lại thread của client thứ 1 thì ta sẽ có thể dùng size đó để đọc dữ liệu vào

